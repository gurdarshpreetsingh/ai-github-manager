import sys

# Check if there are enough arguments
if len(sys.argv) < 2:
    print("Usage: python number_analyzer.py [numbers]")
    sys.exit(1)

# Convert arguments to integers
numbers = [int(arg) for arg in sys.argv[1:]]

# Calculate minimum
min_num = min(numbers)

# Calculate maximum
max_num = max(numbers)

# Calculate average
avg_num = sum(numbers) / len(numbers)

# Print the results
print(f"Minimum: {min_num}")
print(f"Maximum: {max_num}")
print(f"Average: {avg_num}")