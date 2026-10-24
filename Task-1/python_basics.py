"""Day 2: Python basics — variables, data types, input, operators, and functions."""

def calculate_average(numbers):
    """Return the arithmetic mean of a non-empty list of numbers."""
    if not numbers:
        raise ValueError("numbers must not be empty")
    return sum(numbers) / len(numbers)


def main():
    # Variables and common data types
    student_name = "Ranjith"       # str
    internship_day = 2             # int
    hours_per_day = 1.5            # float
    is_learning_ai = True          # bool

    print("Student:", student_name)
    print("Internship day:", internship_day)
    print("Practice hours:", hours_per_day)
    print("Learning AI:", is_learning_ai)

    # Basic arithmetic operators
    first_number = 18
    second_number = 5
    print("\nArithmetic")
    print("Addition:", first_number + second_number)
    print("Subtraction:", first_number - second_number)
    print("Multiplication:", first_number * second_number)
    print("Division:", first_number / second_number)
    print("Floor division:", first_number // second_number)
    print("Remainder:", first_number % second_number)
    print("Power:", first_number ** 2)

    # Strings and type conversion
    age_text = "19"
    age = int(age_text)
    print("\nAge next year:", age + 1)

    # Lists and a user-defined function
    scores = [78, 85, 92, 88]
    print("Scores:", scores)
    print("Average score:", calculate_average(scores))

    # Optional input practice:
    # favourite_language = input("Which programming language are you learning? ")
    # print("You're learning", favourite_language)


if __name__ == "__main__":
    main()
