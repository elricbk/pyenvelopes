import logging
import shutil
import typing as ty

import lxml.etree as etree
from lxml.builder import E  # type: ignore
from lxml.etree import _Element


class AppliedRulesRepository:
    def __init__(self, fname: str) -> None:
        self._items: list[str] = []
        self._fname = fname
        self._load_applied_rules()

    def _load_applied_rules(self) -> None:
        logging.debug("Loading AppliedRules file: %s", self._fname)
        try:
            doc = etree.parse(self._fname)
        except Exception:
            logging.exception("Exception while reading AppliedRules data")
            return

        for el in ty.cast(list[_Element], doc.xpath("//Item")):
            try:
                item = ty.cast(str, el.attrib["weekId"])
                self._items.append(item)
                logging.debug("Found item: %s", item)
            except Exception:
                logging.exception(
                    "Exception while parsing item in AppliedRules data"
                )

    def _save(self) -> None:
        doc = E.RulesApplied()
        doc.extend([E.Item(weekId=item) for item in self._items])
        tmp_fname = self._fname + ".temp"
        try:
            etree.ElementTree(doc).write(tmp_fname, pretty_print=True)
            shutil.move(tmp_fname, self._fname)
        except Exception:
            logging.exception(
                "Exception while saving applied rules information"
            )
            raise

    def rules_applied_for_week(self, week_id: str) -> bool:
        return week_id in self._items

    def mark_week_rules_as_applied(self, week_id: str) -> None:
        self._items.append(week_id)
        self._save()
