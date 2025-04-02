from .xml.expense import ExpenseRepository


def create_expense_repository(fname: str) -> ExpenseRepository:
    """Factory function to create an ExpenseRepository instance."""
    return ExpenseRepository(fname=fname)