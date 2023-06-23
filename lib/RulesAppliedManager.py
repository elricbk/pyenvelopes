import logging
import shutil
import lxml.etree as etree
from lxml.builder import E # type: ignore
import os
from lib import settings

class RulesAppliedManager(object):
    __fileName = os.path.join(settings.data_path, 'rules_applied.xml')

    def __init__(self):
        self.__items = []
        self.__loadAppliedRules()

    def __loadAppliedRules(self):
        logging.debug("Loading AppliedRules file: %s", RulesAppliedManager.__fileName)
        try:
            doc = etree.parse(RulesAppliedManager.__fileName)
        except Exception:
            logging.exception("Exception while reading AppliedRules data")
            return

        for el in doc.xpath("//Item"):
            try:
                item = el.attrib["weekId"]
                self.__items.append(item)
                logging.debug("Found item: %s", item)
            except Exception:
                logging.exception("Exception while parsing item in AppliedRules data")

    def __save(self):
        doc = E.RulesApplied()
        doc.extend([E.Item(weekId=item) for item in self.__items])
        tmpFileName = RulesAppliedManager.__fileName + '.temp'
        try:
            etree.ElementTree(doc).write(tmpFileName, pretty_print=True)
            shutil.move(tmpFileName, RulesAppliedManager.__fileName)
        except Exception:
            logging.exception("Exception while saving applied rules information")
            raise

    def rulesAppliedForWeek(self, weekId):
        return weekId in self.__items

    def markWeekAsRulesApplied(self, weekId):
        self.__items.append(weekId)
        self.__save()
