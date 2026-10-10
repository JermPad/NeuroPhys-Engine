from neurophys.engine import NeuroPhysEngine
from neurophys.loader import load_concepts, load_equations, load_workflows, get_data_path
from neurophys.models import RankedItem


def build_engine() -> NeuroPhysEngine:
    concepts = load_concepts(get_data_path("concepts.json"))
    equations = load_equations(get_data_path("equations.json"))
    workflows = load_workflows(get_data_path("workflows.json"))
    return NeuroPhysEngine(concepts, equations, workflows)


def _rank_label(item_id: str, ranks: dict) -> str:
    rank: RankedItem = ranks.get(item_id)
    if rank is None:
        return ""
    if rank.origin == "query":
        return f"{rank.score:.2f}, query"
    via = f" via {rank.via}" if rank.via else ""
    return f"{rank.score:.2f}, related{via}"


def run_query(query_text: str):
    engine = build_engine()
    results = engine.query(query_text)

    print("Concepts:")
    if results.concepts:
        for concept in results.concepts:
            print(f"- {concept.name} [{concept.category}] ({_rank_label(concept.id, results.ranks)})")
    else:
        print("- None")

    print("\nEquations:")
    if results.equations:
        for equation in results.equations:
            print(
                f"- {equation.name}: {equation.expression} "
                f"({_rank_label(equation.id, results.ranks)})"
            )
    else:
        print("- None")

    print("\nWorkflows:")
    if results.workflows:
        for workflow in results.workflows:
            print(f"- {workflow.name} ({_rank_label(workflow.id, results.ranks)})")
    else:
        print("- None")
