from neurophys.models import QueryResult

class NeuroPhysEngine:
    def __init__(self, concepts, equations, workflows):
        self.concepts = concepts
        self.equations = equations
        self.workflows = workflows

    def query(self, text: str) -> QueryResult:
        query_text = text.lower()

        matched_concepts = [
            concept for concept in self.concepts
            if self._matches(query_text, concept.name, concept.category, concept.tags, concept.notes)
        ]

        matched_equations = [
            equation for equation in self.equations
            if self._matches(query_text, equation.name, equation.expression, equation.variables, equation.tags, equation.notes)
        ]

        matched_workflows = [
            workflow for workflow in self.workflows
            if self._matches(query_text, workflow.name, workflow.steps, workflow.tags, workflow.notes)
        ]

        return QueryResult(
            concepts=matched_concepts,
            equations=matched_equations,
            workflows=matched_workflows,
        )
    
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