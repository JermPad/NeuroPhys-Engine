from typing import Dict, List, Set

import networkx as nx

from neurophys.models import QueryResult, RankedItem

ACTIVATION_DECAY = 0.5
MAX_HOPS = 2


class NeuroPhysEngine:
    def __init__(self, concepts, equations, workflows):
        self.concepts = concepts
        self.equations = equations
        self.workflows = workflows
        self._by_id = {item.id: item for item in [*concepts, *equations, *workflows]}
        self.graph = self._build_graph()

    def query(self, text: str) -> QueryResult:
        query_text = text.lower()

        seed_ids = {
            concept.id
            for concept in self.concepts
            if self._matches(query_text, concept.name, concept.category, concept.tags, concept.notes)
        }
        seed_ids.update(
            equation.id
            for equation in self.equations
            if self._matches(
                query_text,
                equation.name,
                equation.expression,
                equation.variables,
                equation.tags,
                equation.notes,
            )
        )
        seed_ids.update(
            workflow.id
            for workflow in self.workflows
            if self._matches(query_text, workflow.name, workflow.steps, workflow.tags, workflow.notes)
        )

        ranks = self._spread_activation(seed_ids)
        scored_ids = [node_id for node_id, rank in sorted(ranks.items(), key=lambda item: (-item[1].score, item[0]))]

        return QueryResult(
            concepts=[self._by_id[node_id] for node_id in scored_ids if node_id in self._concept_ids()],
            equations=[self._by_id[node_id] for node_id in scored_ids if node_id in self._equation_ids()],
            workflows=[self._by_id[node_id] for node_id in scored_ids if node_id in self._workflow_ids()],
            ranks=ranks,
        )

    def _spread_activation(self, seed_ids: Set[str]) -> Dict[str, RankedItem]:
        ranks: Dict[str, RankedItem] = {}
        for seed_id in seed_ids:
            if seed_id not in self.graph:
                continue
            ranks[seed_id] = RankedItem(score=1.0, origin="query", hops=0)
            paths = nx.single_source_shortest_path(self.graph, seed_id, cutoff=MAX_HOPS)
            for node_id, path in paths.items():
                hops = len(path) - 1
                if hops == 0:
                    continue
                score = ACTIVATION_DECAY ** hops
                current = ranks.get(node_id)
                if current is None or score > current.score:
                    ranks[node_id] = RankedItem(
                        score=score,
                        origin="activation",
                        via=self._by_id[path[-2]].name,
                        hops=hops,
                    )
        return ranks

    def _build_graph(self) -> nx.Graph:
        graph = nx.Graph()
        for item in [*self.concepts, *self.equations, *self.workflows]:
            graph.add_node(item.id)

        for concept in self.concepts:
            self._link(graph, concept.id, concept.related_concepts)
            self._link(graph, concept.id, concept.related_equations)

        for equation in self.equations:
            self._link(graph, equation.id, equation.related_concepts)
            self._link(graph, equation.id, getattr(equation, "related_equations", []))

        for workflow in self.workflows:
            self._link(graph, workflow.id, workflow.related_concepts)
            self._link(graph, workflow.id, workflow.related_equations)

        return graph

    def _link(self, graph: nx.Graph, source_id: str, target_ids: List[str]) -> None:
        for target_id in target_ids:
            if target_id in graph:
                graph.add_edge(source_id, target_id)

    def _concept_ids(self) -> Set[str]:
        return {item.id for item in self.concepts}

    def _equation_ids(self) -> Set[str]:
        return {item.id for item in self.equations}

    def _workflow_ids(self) -> Set[str]:
        return {item.id for item in self.workflows}

    def _matches(self, query_text: str, *fields) -> bool:
        searchable_text = " ".join(self._flatten_fields(fields)).lower()
        return all(word in searchable_text for word in query_text.split())

    def _flatten_fields(self, fields):
        flattened = []
        for field in fields:
            if isinstance(field, list):
                flattened.extend(str(item) for item in field)
            else:
                flattened.append(str(field))
        return flattened
