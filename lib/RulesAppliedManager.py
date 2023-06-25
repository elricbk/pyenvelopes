import logging
import os
import shutil
import typing as ty

import lxml.etree as etree
from lxml.builder import E  # type: ignore
from lxml.etree import _Element

from lib import settings


class RulesAppliedManager:
    __fileName = os.path.join(settings.data_path, "rules_applied.xml")

    def __init__(self) -> None:
        self.__items: list[str] = []
        self.__loadAppliedRules()

    def __loadAppliedRules(self) -> None:
        logging.debug(
            "Loading AppliedRules file: %s", RulesAppliedManager.__fileName
        )
        try:
            doc = etree.parse(RulesAppliedManager.__fileName)
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
        tmpFileName = RulesAppliedManager.__fileName + ".temp"
        try:
            etree.ElementTree(doc).write(tmpFileName, pretty_print=True)
            shutil.move(tmpFileName, RulesAppliedManager.__fileName)
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
