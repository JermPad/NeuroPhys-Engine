from neurophys.engine import NeuroPhysEngine
from neurophys.loader import load_concepts, load_equations, load_workflows, get_data_path

def build_engine() -> NeuroPhysEngine:
    concepts = load_concepts(get_data_path("concepts.json"))
    equations = load_equations(get_data_path("equations.json"))
    workflows = load_workflows(get_data_path("workflows.json"))
    return NeuroPhysEngine(concepts, equations, workflows)

def run_query(query_text: str):
    engine = build_engine()
    results = engine.query(query_text)

    print("Concepts:")
    if results.concepts:
        for concept in results.concepts:
            print(f"- {concept.name} [{concept.category}]")
    else:
        print("- None")

    print("\nEquations:")
    if results.equations:
        for equation in results.equations:
            print(f"- {equation.name}: {equation.expression}")
    else:
        print("- None")

    print("\nWorkflows:")
    if results.workflows:
        for workflow in results.workflows:
            print(f"- {workflow.name}")
    else:
        print("- None")