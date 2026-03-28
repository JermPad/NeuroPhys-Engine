import json
from pathlib import Path
from typing import List

from neurophys.models import Concept, Equation, Workflow

def load_json_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def load_concepts(path: str) -> List[Concept]:
    raw_data = load_json_file(path)
    return [Concept(**item) for item in raw_data]

def load_equations(path: str) -> List[Equation]:
    raw_data = load_json_file(path)
    return [Equation(**item) for item in raw_data]

def load_workflows(path: str) -> str:
    raw_data = load_json_file(path)
    return [Workflow(**item) for item in raw_data]

def get_data_path(filename: str) -> str:
    project_root = Path(__file__).resolve().parent.parent
    return str(project_root / "data" / filename)