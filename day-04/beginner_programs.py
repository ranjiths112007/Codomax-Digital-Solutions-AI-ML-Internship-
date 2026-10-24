"""Day 4: Small beginner-friendly Python programs.

Run this file with:
    python day-04/beginner_programs.py
"""


def is_even(number):
    """Return True when number is even."""
    return number % 2 == 0


def factorial(number):
    """Return n! for a non-negative integer n."""
    if not isinstance(number, int) or isinstance(number, bool):
        raise TypeError("number must be an integer")
    if number < 0:
        raise ValueError("number must be non-negative")

    result = 1
    for value in range(2, number + 1):
        result *= value
    return result


def is_palindrome(text):
    """Check whether text reads the same forwards and backwards.

    Spaces and punctuation are ignored, and comparison is case-insensitive.
    """
    cleaned = "".join(character.lower() for character in text if character.isalnum())
    return cleaned == cleaned[::-1]


def simple_calculator(first, operator, second):
    """Perform one of the four basic arithmetic operations."""
    if operator == "+":
        return first + second
    if operator == "-":
        return first - second
    if operator == "*":
        return first * second
    if operator == "/":
        if second == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return first / second
    raise ValueError("Operator must be one of: +, -, *, /")


def main():
    print("1. Even or odd")
    for number in [2, 7, 10, 13]:
        print(f"{number} is {'even' if is_even(number) else 'odd'}")

    print("\n2. Multiplication table for 5")
    for multiplier in range(1, 11):
        print(f"5 x {multiplier} = {5 * multiplier}")

    print("\n3. Factorial")
    print("5! =", factorial(5))

    print("\n4. Palindrome")
    phrase = "Never odd or even"
    print(f"{phrase!r} is a palindrome:", is_palindrome(phrase))

    print("\n5. Simple calculator")
    print("12 + 4 =", simple_calculator(12, "+", 4))
    print("12 - 4 =", simple_calculator(12, "-", 4))
    print("12 * 4 =", simple_calculator(12, "*", 4))
    print("12 / 4 =", simple_calculator(12, "/", 4))

    print("\n6. List summary")
    numbers = [14, 3, 27, 8, 19]
    print("Numbers:", numbers)
    print("Minimum:", min(numbers))
    print("Maximum:", max(numbers))
    print("Sum:", sum(numbers))
    print("Average:", sum(numbers) / len(numbers))


if __name__ == "__main__":
    main()
