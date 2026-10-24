"""Day 3: Conditions, loops, lists, and basic problem-solving."""


def classify_mark(mark):
    """Return a simple grade label for a mark between 0 and 100."""
    if not isinstance(mark, (int, float)) or isinstance(mark, bool):
        raise TypeError("mark must be a number")
    if not 0 <= mark <= 100:
        raise ValueError("mark must be between 0 and 100")

    if mark >= 90:
        return "A"
    elif mark >= 75:
        return "B"
    elif mark >= 60:
        return "C"
    elif mark >= 40:
        return "D"
    return "Needs improvement"


def main():
    # if / elif / else
    mark = 84
    print(f"Mark {mark}: Grade {classify_mark(mark)}")

    # for loop
    print("\nNumbers from 1 to 5:")
    for number in range(1, 6):
        print(number)

    # while loop
    print("\nCountdown:")
    count = 3
    while count > 0:
        print(count)
        count -= 1
    print("Go!")

    # Lists: access, append, remove, sort, and iterate
    languages = ["Python", "Java", "JavaScript"]
    languages.append("SQL")
    print("\nLanguages:", languages)
    print("First language:", languages[0])

    languages.remove("Java")
    languages.sort()
    print("After removing Java and sorting:", languages)

    print("\nList items:")
    for language in languages:
        print("-", language)

    # List comprehension
    squares = [number ** 2 for number in range(1, 6)]
    print("Squares:", squares)

    # Simple accumulator
    values = [12, 7, 19, 4, 10]
    total = 0
    for value in values:
        total += value
    print("Values:", values)
    print("Total:", total)
    print("Largest value:", max(values))


if __name__ == "__main__":
    main()
