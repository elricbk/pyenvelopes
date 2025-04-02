import typing as ty
from .xml.expense_rule import ExpenseRuleRepository
# Need ExpenseRepository for type hint and passing to constructor
from ..expense import create_expense_repository, ExpenseRepository


def create_expense_rule_repository(
    fname: str, expenses: ExpenseRepository
) -> ExpenseRuleRepository:
    """Factory function to create an ExpenseRuleRepository instance."""
    return ExpenseRuleRepository(fname=fname, expenses=expenses)