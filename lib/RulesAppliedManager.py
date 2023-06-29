import logging
import shutil
import typing as ty

import lxml.etree as etree
from lxml.builder import E  # type: ignore
from lxml.etree import _Element


class RulesAppliedManager:
    def __init__(self, fname: str) -> None:
        self.__items: list[str] = []
        self._fname = fname
        self.__loadAppliedRules()

    def __loadAppliedRules(self) -> None:
        logging.debug("Loading AppliedRules file: %s", self._fname)
        try:
            doc = etree.parse(self._fname)
        except Exception:
            logging.exception("Exception while reading AppliedRules data")
            return

        for el in ty.cast(list[_Element], doc.xpath("//Item")):
            try:
                item = ty.cast(str, el.attrib["weekId"])
                self.__items.append(item)
                logging.debug("Found item: %s", item)
            except Exception:
                logging.exception(
                    "Exception while parsing item in AppliedRules data"
                )

    def __save(self) -> None:
        doc = E.RulesApplied()
        doc.extend([E.Item(weekId=item) for item in self.__items])
        tmpFileName = self._fname + ".temp"
        try:
            etree.ElementTree(doc).write(tmpFileName, pretty_print=True)
            shutil.move(tmpFileName, self._fname)
        except Exception:
            logging.exception(
                "Exception while saving applied rules information"
            )
            raise

    def rulesAppliedForWeek(self, weekId: str) -> bool:
        return weekId in self.__items

    def markWeekAsRulesApplied(self, weekId: str) -> None:
        self.__items.append(weekId)
        self.__save()
