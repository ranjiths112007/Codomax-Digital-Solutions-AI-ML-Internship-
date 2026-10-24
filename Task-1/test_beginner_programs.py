"""Basic unit tests for beginner_programs.py."""
import unittest

from beginner_programs import factorial, is_even, is_palindrome, simple_calculator


class BeginnerProgramsTests(unittest.TestCase):
    def test_even_odd(self):
        self.assertTrue(is_even(10))
        self.assertFalse(is_even(7))

    def test_factorial(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(5), 120)

    def test_factorial_rejects_negative(self):
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_palindrome(self):
        self.assertTrue(is_palindrome("Never odd or even"))
        self.assertFalse(is_palindrome("Python"))

    def test_calculator(self):
        self.assertEqual(simple_calculator(2, "+", 3), 5)
        self.assertEqual(simple_calculator(7, "-", 2), 5)
        self.assertEqual(simple_calculator(4, "*", 3), 12)
        self.assertEqual(simple_calculator(8, "/", 2), 4)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            simple_calculator(1, "/", 0)


if __name__ == "__main__":
    unittest.main()
