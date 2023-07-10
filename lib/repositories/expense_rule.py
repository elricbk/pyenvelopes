import logging
import typing as ty
import uuid

from lxml import etree
from lxml.builder import E  # type: ignore
from lxml.etree import _Element

from lib.models.expense_rule import ExpenseRule

from .expense import ExpenseRepository


class ExpenseRuleRepository:
    def __init__(self, fname: str, expenses: ExpenseRepository) -> None:
        self.rules: ty.Final[list[ExpenseRule]] = []
        self._expense_repository = expenses
        self._fname = fname
        self._load()

    def _save(self) -> None:
        doc = E.ExpenseRules()
        doc.extend([rule.to_xml() for rule in self.rules])
        fname = self._fname
        etree.ElementTree(doc).write(fname, encoding="utf-8", pretty_print=True)

    def _load(self) -> None:
        try:
            doc = etree.parse(self._fname)
        except Exception:
            logging.exception("Exception while reading ExpenseRule datafile")
            return

        for el in ty.cast(list[_Element], doc.xpath("//ExpenseRule")):
            try:
                self.rules.append(ExpenseRule.from_xml(el))
            except Exception:
                logging.exception("Exception while parsing ExpenseRule")

    def add_rule(self, amount: float, from_id: int, to_id: int) -> ExpenseRule:
        rule = ExpenseRule(uuid.uuid4(), amount, from_id, to_id)
        self.rules.append(rule)
        self._save()
        return rule

    def clear(self) -> None:
        self.rules.clear()

    def _execute_rule(self, rule: ExpenseRule) -> None:
        self._expense_repository.add_expense_for_rule(
            rule.amount, rule.from_id, rule.to_id
        )

    def execute_all_rules(self) -> None:
        # FIXME: this triggers expense saving for each rule instead of saving once
        for rule in self.rules:
            self._execute_rule(rule)
