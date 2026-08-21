import sys

def main():
    # Check if there are enough command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python number_analyzer.py <number>")
        return

    # Read numbers from command-line arguments
    numbers = [float(arg) for arg in sys.argv[1:]]

    # Calculate minimum
    min_number = min(numbers)

    # Calculate maximum
    max_number = max(numbers)

    # Calculate average
    average = sum(numbers) / len(numbers)

    # Print the results
    print(f"Minimum: {min_number}")
    print(f"Maximum: {max_number}")
    print(f"Average: {average}")

if __name__ == "__main__":
    main()