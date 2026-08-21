import sys

def main():
    # Read numbers from command-line arguments
    numbers = [float(arg) for arg in sys.argv[1:] if arg.isdigit()]
    
    if not numbers:
        print("No valid numbers provided.")
        return
    
    # Calculate minimum
    min_num = min(numbers)
    
    # Calculate maximum
    max_num = max(numbers)
    
    # Calculate average
    avg_num = sum(numbers) / len(numbers)
    
    # Print results clearly
    print(f"Minimum: {min_num}")
    print(f"Maximum: {max_num}")
    print(f"Average: {avg_num}")

if __name__ == "__main__":
    main()