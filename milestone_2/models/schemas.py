from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class TicketInput:
    id: str
    title: str
    description: str
    category: str
    priority: str
    employee_name: Optional[str] = "Employee"
    email: Optional[str] = "employee@company.com"

@dataclass
class KBArticle:
    id: str
    title: str
    category: str
    content: str
    score: float = 0.0

@dataclass
class WorkflowStep:
    name: str
    status: str
    elapsed_ms: float
    timestamp: str