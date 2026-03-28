from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Concept:
    id: str
    name: str
    category: str
    tags: List[str] = field(default_factory=list)
    related_equations: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    notes: str = ""

@dataclass
class Equation:
    id: str
    name: str
    expression: str
    variables: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    notes: str = ""

@dataclass
class Workflow:
    id: str
    name: str
    steps: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    related_equations: List[str] = field(default_factory=list)
    notes: str = ""

@dataclass
class QueryResult:
    concepts: List[Concept]
    equations: List[Equation]
    workflows: List[Workflow]