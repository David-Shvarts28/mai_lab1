import unittest
from src.calc import shunting_yard, CalcError



class TestShuntingYard(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(shunting_yard("1 + 2 * 3"), 7)
        self.assertEqual(shunting_yard("(1 + 2) * 3"), 9)
        self.assertEqual(shunting_yard("10 / 4"), 2.5)

    def test_unary(self):
        self.assertEqual(shunting_yard("2**3**2"), 512)
        self.assertEqual(shunting_yard("(-2)**2"), 4)
        self.assertEqual(shunting_yard("-2**2"), 4)

    def test_integer(self):
        self.assertEqual(shunting_yard("10 // 3"), 3)
        self.assertEqual(shunting_yard("1 // -2"), -1)
        self.assertEqual(shunting_yard("10 % 3"), 1)
        self.assertEqual(shunting_yard("1.5 * 2"), 3)
        self.assertEqual(shunting_yard("1.5 / 3"), 0.5)
        self.assertEqual(shunting_yard("5 / 1"), 5.0)



    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            shunting_yard("10 / 0")
        with self.assertRaises(ZeroDivisionError):
            shunting_yard("10 % 0")
        with self.assertRaises(ZeroDivisionError):
            shunting_yard("10 // 0")

    def test_operators_non_integers(self):
        with self.assertRaisesRegex(CalcError, "Операторы '//' требуют целых чисел."):
            shunting_yard("5.5 // 2")
        with self.assertRaisesRegex(CalcError, "Операторы '//' требуют целых чисел."):
            shunting_yard("5 // 2.5")
        with self.assertRaisesRegex(CalcError, "Операторы '%' требуют целых чисел."):
            shunting_yard("10 % 2.5")

    def test_parentheses(self):
        with self.assertRaisesRegex(CalcError, "Несбалансированные скобки"):
            shunting_yard("(1 + 2))")
        with self.assertRaisesRegex(CalcError, "Несбалансированные скобки"):
            shunting_yard("(1 + 2")
        with self.assertRaisesRegex(CalcError, "Несбалансированные скобки"):
            shunting_yard("1 + 2)")

    def test_unary_context(self):
        self.assertEqual(shunting_yard("2 * -5"), -10)
        self.assertEqual(shunting_yard("10 / +2"), 5)
        self.assertEqual(shunting_yard("2 ** -3"), 0.125)

    def test_required(self):
        error= r"Унарный оператор '-' не может следовать за '-'. Используйте скобки."
        with self.assertRaisesRegex(CalcError, error):
            shunting_yard("2 - - 2")
        error = r"Унарный оператор '-' не может следовать за '-'. Используйте скобки."
        with self.assertRaisesRegex(CalcError, error):
            shunting_yard("- - 2")
        error = r"Унарный оператор '\+' не может следовать за '\+'. Используйте скобки."
        with self.assertRaisesRegex(CalcError, error):
            shunting_yard("2 + + 2")
        error = r"Унарный оператор '\-' не может следовать за '\+'. Используйте скобки."
        with self.assertRaisesRegex(CalcError, error):
            shunting_yard("2 + - 2")
        error = r"Унарный оператор '\+' не может следовать за '\-'. Используйте скобки."
        with self.assertRaisesRegex(CalcError, error):
            shunting_yard("2 - + 2")

        self.assertEqual(shunting_yard("2 + (-2)"), 0)
        self.assertEqual(shunting_yard("2 - (-2)"), 4)
        self.assertEqual(shunting_yard("+5 - 3"), 2)



    def test_syntax_and_operand_errors(self):
        with self.assertRaisesRegex(CalcError, "Недостаточно операндов."):
            shunting_yard("1 + 2 +")
        with self.assertRaisesRegex(CalcError, "Недостаточно операндов."):
            shunting_yard("1 + 2 +")
        with self.assertRaisesRegex(CalcError, "Пустое выражение."):
            shunting_yard(" ")
        with self.assertRaisesRegex(CalcError, "Некорректное выражение."):
            shunting_yard("()")

    def test_recognize(self):
        with self.assertRaisesRegex(CalcError, r"Неизвестный токен."):
            shunting_yard("1 $ 2")
        with self.assertRaisesRegex(CalcError, r"Неизвестный токен."):
            shunting_yard("1 + # 2")

    def test_invalid_unary_sequence_errors(self):
        error_regex_triple = r"Недопустимая последовательность идущих подряд унарных\/простых операторов."
        with self.assertRaisesRegex(CalcError, error_regex_triple):
            shunting_yard("2 - - - 3")
        with self.assertRaisesRegex(CalcError, error_regex_triple):
            shunting_yard("2 + + - 3")


if __name__ == '__main__':
    unittest.main()
