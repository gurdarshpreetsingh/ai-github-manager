import sys
from typing import List

def analyze_numbers(numbers: List[float]) -> None:
    if not numbers:
        print("No numbers provided.")
        return

    min_num = min(numbers)
    max_num = max(numbers)
    avg_num = sum(numbers) / len(numbers)

    print(f"Minimum number: {min_num}")
    print(f"Maximum number: {max_num}")
    print(f"Average number: {avg_num}")

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python number_analyzer.py <number1> <number2> ...")
        return

    numbers = [float(num) for num in sys.argv[1:]]
    analyze_numbers(numbers)

if __name__ == "__main__":
    main()