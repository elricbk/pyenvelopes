import typing as ty
from .xml.envelope import EnvelopeRepository
from ..expense import ExpenseRepository  # Need type hint


def create_envelope_repository(fname: str) -> EnvelopeRepository:
    """Factory function to create an EnvelopeRepository instance."""
    repo = EnvelopeRepository(fname=fname)
    # Note: ExpenseRepository dependency is injected later via set_expense_repository
    return repo