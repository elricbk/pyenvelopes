from lib.parse_expense import parse_expense

import unittest

class TestParseExpense(unittest.TestCase):
    def test_parse_expense__given_full_form_line__parses_it(self):
        line = '42 moving money %корзина %доход'

        result = parse_expense(line)

        self.assertEqual(result.amount, '42')
        self.assertEqual(result.comment, 'moving money')
        self.assertEqual(result.from_envelope, 'корзина')
        self.assertEqual(result.to_envelope, 'доход')

    def test_parse_expense__given_expense_from_envelope__parses_it(self):
        line = '24 spending money %запас'

        result = parse_expense(line)

        self.assertEqual(result.amount, '24')
        self.assertEqual(result.comment, 'spending money')
        self.assertEqual(result.from_envelope, 'запас')
        self.assertEqual(result.to_envelope, 'корзина')

    def test_parse_expense__given_income_to_envelope__parses_it(self):
        line = '+84 getting money %envelope'

        result = parse_expense(line)

        self.assertEqual(result.amount, '84')
        self.assertEqual(result.comment, 'getting money')
        self.assertEqual(result.from_envelope, 'доход')
        self.assertEqual(result.to_envelope, 'envelope')

    def test_parse_expense__given_short_form__parses_it(self):
        line = '42 short form'

        result = parse_expense(line)

        self.assertEqual(result.amount, '42')
        self.assertEqual(result.comment, 'short form')
        self.assertIsNone(result.from_envelope)
        self.assertEqual(result.to_envelope, 'корзина')

    def test_parse_expense__given_unknown_line__throws(self):
        with self.assertRaises(Exception):
            parse_expense('wrong format line')

if __name__ == '__main__':
    unittest.main()
