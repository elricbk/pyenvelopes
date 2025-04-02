import uuid
from dataclasses import dataclass


@dataclass
class ExpenseRule:
    id: uuid.UUID
    amount: float
    from_id: int
    to_id: int
