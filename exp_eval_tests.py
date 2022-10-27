# Start of unittest - add to completely test functions in exp_eval!

import unittest
from exp_eval import *


class test_expressions(unittest.TestCase):

    def test_postfix_eval_01a(self) -> None:
        self.assertAlmostEqual(postfix_eval("3 5 +"), 8)

    def test_postfix_eval_01b(self) -> None:
        self.assertAlmostEqual(postfix_eval("8 1 >>"), 4)
        self.assertAlmostEqual(postfix_eval("8 1 <<"), 16)

    def test_postfix_eval_01c(self) -> None:
        self.assertAlmostEqual(postfix_eval("8 2 **"), 64)

    def test_postfix_eval_01d(self) -> None:
        self.assertAlmostEqual(postfix_eval("18.5 -2 *"), -37)
        self.assertAlmostEqual(postfix_eval("-18.52 -0.78 +"), -19.3)

    def test_postfix_eval_02(self) -> None:
        try:
            postfix_eval("blah")
            self.fail()     # pragma: no cover
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Invalid token")

    def test_postfix_eval_03a(self) -> None:
        try:
            postfix_eval("4 +")
            self.fail()     # pragma: no cover
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")

    def test_postfix_eval_03b(self) -> None:
        try:
            postfix_eval("")
            self.fail()     # pragma: no cover
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")

    def test_postfix_eval_04(self) -> None:
        try:
            postfix_eval("1 2 3 +")
            self.fail()     # pragma: no cover
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Too many operands")

    def test_postfix_eval_illegal_bitshift(self) -> None:
        try:
            postfix_eval("1 3.3 >>")
            self.fail()  # pragma: no cover
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Illegal bit shift operand")
        try:
            postfix_eval("1 3.3 <<")
            self.fail()  # pragma: no cover
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Illegal bit shift operand")

    def test_postfix_eval_divide_by_0(self) -> None:
        with self.assertRaises(ValueError):
            postfix_eval("0 0 /")

    def test_postfix_eval_bad_format(self) -> None:
        try:
            postfix_eval("1 + 1")
            self.fail()  # pragma: no cover
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Bad post-fix format")

    def test_postfix_eval_every_operand(self) -> None:
        self.assertEqual(postfix_eval("2 2 **"), postfix_eval("2 1 <<"))
        self.assertEqual(postfix_eval("2 2 /"), postfix_eval("2 1 >>"))
        self.assertAlmostEqual(postfix_eval("3 2 << 2 / 1 >> .7 3 * + 3 2 ** -"), -3.9)

    def test_infix_to_postfix_01a(self) -> None:
        self.assertEqual(infix_to_postfix("6 - 3"), "6 3 -")
        self.assertEqual(infix_to_postfix("6"), "6")
        self.assertEqual(infix_to_postfix("32 >> 2 >> 1"), "32 2 >> 1 >>")


    def test_infix_to_postfix_01b(self) -> None:
        self.assertEqual(infix_to_postfix("32 >> 2 << 1"), "32 2 >> 1 <<")

    def test_infix_to_postfix_01c(self) -> None:
        self.assertEqual(infix_to_postfix("3 ** 2 ** 2"), "3 2 2 ** **")

    def test_infix_to_postfix_02(self) -> None:
        self.assertEqual(infix_to_postfix("( 5 - 3 ) * 4"), "5 3 - 4 *")
        self.assertEqual(infix_to_postfix("3 + 4 * 2 / ( 1 - 5 ) ** 2 ** 3"), "3 4 2 * 1 5 - 2 3 ** ** / +")

    def test_infix_to_postfix_03(self) -> None:
        self.assertEqual(infix_to_postfix("70 - -3 * 10"), "70 -3 10 * -")

    def test_infix_to_postfix_04(self) -> None:
        self.assertEqual(infix_to_postfix("70.52 - 3.5 * 10.05"), "70.52 3.5 10.05 * -")

    def test_infix_to_postfix_05(self) -> None:
        self.assertEqual(infix_to_postfix("-70.52 - 3.5 * 10.05"), "-70.52 3.5 10.05 * -")

    def test_infix_to_postfix_right_assc(self) -> None:
        self.assertEqual(infix_to_postfix("2 ** 3 ** ( 2 + 1 )"), "2 3 2 1 + ** **")

    def test_prefix_to_postfix(self) -> None:
        self.assertEqual(prefix_to_postfix("* - 3 / 2 1 - / 4 5 6"), "3 2 1 / - 4 5 / 6 - *")

    def test_prefix_all_ops(self) -> None:
        self.assertEqual(prefix_to_postfix("** + - * / >> << 1 2 3 4 5 6 7 8"), "1 2 << 3 >> 4 / 5 * 6 - 7 + 8 **")
        self.assertEqual(postfix_eval(prefix_to_postfix("** + - * / >> << 1 2 3 4 5 6 7 8")), 1)

    def test_passing_in_1_num(self) -> None:
        self.assertEqual(postfix_eval("3.14"), 3.14)
        try:
            postfix_eval("3.14 ")
            self.fail()     # pragma: no cover
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Invalid token")
        self.assertEqual(infix_to_postfix("3.14"), "3.14")
        self.assertEqual(prefix_to_postfix("3.14"), "3.14")
        # although methods are assumed to have valid inputs, they also work without
        self.assertEqual(infix_to_postfix(""), "")
        self.assertEqual(prefix_to_postfix(""), "")

    def test_all_notation_eval(self) -> None:
        self.assertEqual(infix_to_postfix("( 3 + 2 ) - 9 * 3 << 2"), "3 2 + 9 3 2 << * -")
        self.assertEqual(prefix_to_postfix("- + 3 2 * 9 << 3 2"), "3 2 + 9 3 2 << * -")
        self.assertEqual(postfix_eval(infix_to_postfix("( 3 + 2 ) - 9 * 3 << 2")), -103)
        self.assertEqual(postfix_eval(prefix_to_postfix("- + 3 2 * 9 << 3 2")), -103)
        self.assertEqual(postfix_eval("3 2 + 9 3 2 << * -"), -103)

    def test_eval_parentheses(self) -> None:
        self.assertEqual(infix_to_postfix("( 3 + 4 * 5 ) * 7"), "3 4 5 * + 7 *")
        self.assertEqual(infix_to_postfix("( 3 * 4 + 5 ) * 7"), "3 4 * 5 + 7 *")
        self.assertEqual(postfix_eval(infix_to_postfix("( 3 + 4 * 5 ) * 7")), 161)
        self.assertEqual(postfix_eval(infix_to_postfix("( 3 * 4 + 5 ) * 7")), 119)
        self.assertEqual(infix_to_postfix("3 * 4 + 5 * 7"), "3 4 * 5 7 * +")

if __name__ == "__main__":
    unittest.main()
