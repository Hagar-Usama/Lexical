import unittest
from helpers.RegExp import RegExp

class TestRegExp(unittest.TestCase):

    def test_regex_input(self):

        case = 'test regex input [case 1]'

        operators = {'(', ')', '*', '|'}
        exp = "(a|bc)*#"
        exp = list(exp)
        r = RegExp(exp, operators, star="*")

        actual_value = r.handle_exp()
        correct_value = ['(', 'a', '|', 'b', 'CONCAT', 'c', ')',
                        '*', 'CONCAT', '#']
        self.assertEqual(actual_value, correct_value, case)

if __name__ == '__main__':
    unittest.main()
