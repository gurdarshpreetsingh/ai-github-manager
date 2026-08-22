import sys

if len(sys.argv) < 2:
    print("Please provide at least one number.")
    sys.exit(1)

numbers = []
for arg in sys.argv[1:]:
    if not arg.isdigit():
        print("All arguments must be numbers.")
        sys.exit(1)
    numbers.append(float(arg))

min_num = min(numbers)
max_num = max(numbers)
average = sum(numbers) / len(numbers)

print(f"Minimum: {min_num}")
print(f"Maximum: {max_num}")
print(f"Average: {average}")

print(unknown_variable)