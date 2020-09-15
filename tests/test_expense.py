from Expense import Expense

from lxml import etree
import datetime
import unittest
import uuid

class TestExpense(unittest.TestCase):
    def test_to_xml__always__serializes_expense(self):
        expense = Expense(uuid.uuid4(), datetime.datetime.now(), 42, '', 0, 0)

        result = expense.toXml()

        self.assertEqual(result.attrib['id'], str(expense.id))
        self.assertEqual(result.attrib['manual'], "True")

    def test_from_xml__given_serialized_expense__loads_it(self):
        data = '''<Expense
            id="18844fd6-358b-4d82-8eaf-dcf536771e81"
            date="2020-03-09 13:35:00"
            value="42.0"
            desc="Automatic creation of weekly envelope"
            fromId="3"
            toId="4"
            line=""
            manual="False"
        />'''

        expense = Expense.fromXml(etree.fromstring(data))

        self.assertEqual(int(expense.value), 42)
        self.assertEqual(expense.fromId, 3)
        self.assertEqual(expense.toId, 4)

    def test_expense__always__can_be_used_as_map_key(self):
        expense = Expense(uuid.uuid4(), datetime.datetime.now(), 42, '', 0, 0)
        data = {}

        data[expense] = 4

        self.assertEqual(data[expense], 4)


if __name__ == '__main__':
    unittest.main()