import random
import time
import os

from heap_sort import heap_sort
from merge_sort import merge_sort
from database import create_database, get_new_session_id, save_result
from analysis import show_all_results, show_session_results, show_complexity

MAX_SIZE = 200000


# Generates randomized financial transaction data
# Random test includes a mix of integers and floating-point values
def generate_transactions(size):
    transactions = []

    for _ in range(size):
        if random.choice([True, False]):
            transactions.append(random.randint(1, 10000))
        else:
            transactions.append(round(random.uniform(1.0, 10000.0), 2))

    return transactions


# Converts a text value into either int or float
def convert_number(value):
    if "." in value:
        return float(value)
    return int(value)


# Loads multiple transaction lists from a file
def load_transactions_from_file(filename):
    datasets = []
    current_list = []

    try:
        with open(filename, "r") as file:
            for line in file:
                value = line.strip()

                if value == "":
                    if current_list:
                        datasets.append(current_list)
                        current_list = []
                    continue

                current_list.append(convert_number(value))

            # Add the last dataset if the file does not end with a blank line
            if current_list:
                datasets.append(current_list)

        return datasets

    except FileNotFoundError:
        print("File not found. Make sure the file name or path is correct.\n")
        return None

    except ValueError:
        print("Invalid data inside file. Use only integers or decimals.\n")
        return None

# Displays an array with a title, showing only the first few items if it's too long
def display_array(title, arr, limit=MAX_SIZE):
    print(f"\n{title}")

    if len(arr) <= limit:
        print(arr)
    else:
        print(arr[:limit])

# Measures the execution time of a sorting algorithm and returns both the time and sorted result
def time_algorithm(func, data):
    start = time.perf_counter()
    result = func(data)
    end = time.perf_counter()

    return end - start, result

# Determines which sorting algorithm was faster or if it was a tie
def get_faster(m_time, h_time):
    if m_time < h_time:
        return "Merge Sort"
    elif h_time < m_time:
        return "Heap Sort"
    return "Tie"

# Runs a sorting test using randomly generated mixed transactions
def run_random_test(session_id):
    size = random.randint(1, MAX_SIZE)
    transactions = generate_transactions(size)

    display_array("Original Random Transactions:", transactions)

    print("\nRunning sorting algorithms...\n")

    m_time, m_sorted = time_algorithm(merge_sort, transactions.copy())
    h_time, h_sorted = time_algorithm(heap_sort, transactions.copy())

    display_array("Sorted Random Transactions:", m_sorted)

    faster = get_faster(m_time, h_time)

    print("\nResults")
    print("-" * 40)
    print(f"Session ID: {session_id}")
    print(f"Size: {size}")
    print("Input Type: Randomized")
    print(f"Merge Sort Time: {m_time:.8f}")
    print(f"Heap Sort Time:  {h_time:.8f}")
    print(f"Faster Algorithm: {faster}")

    if m_sorted == h_sorted:
        save_result(session_id, size, "random_mixed", m_time, h_time, faster)
        print("Result saved to database.\n")
    else:
        print("Sorting mismatch. Result not saved.\n")


# Runs a sorting test using user-provided input from the console
def run_custom_test(session_id):
    user_input = input("Enter numbers separated by spaces: ")

    try:
        arr = []

        for value in user_input.split():
            arr.append(convert_number(value))

    except ValueError:
        print("Invalid input. Please enter valid integers or decimals.\n")
        return

    if len(arr) == 0:
        print("No values entered.\n")
        return

    display_array("Original Custom Array:", arr)

    print("\nRunning sorting algorithms...\n")

    m_time, m_sorted = time_algorithm(merge_sort, arr.copy())
    h_time, h_sorted = time_algorithm(heap_sort, arr.copy())

    display_array("Sorted Custom Array:", m_sorted)

    faster = get_faster(m_time, h_time)

    print("\nResults")
    print("-" * 40)
    print(f"Session ID: {session_id}")
    print(f"Size: {len(arr)}")
    print("Input Type: Custom")
    print(f"Merge Sort Time: {m_time:.8f}")
    print(f"Heap Sort Time:  {h_time:.8f}")
    print(f"Faster Algorithm: {faster}")

    if m_sorted == h_sorted:
        save_result(session_id, len(arr), "custom", m_time, h_time, faster)
        print("Result saved to database.\n")
    else:
        print("Sorting mismatch. Result not saved.\n")


# Runs tests using datasets loaded from a file, allowing multiple datasets in one file
def run_file_test(session_id):

    filename = input("Enter file name or full path: ").strip()

    # Automatically check project folder first
    if not os.path.isfile(filename):

        local_path = os.path.join(os.getcwd(), filename)

        if os.path.isfile(local_path):
            filename = local_path

        else:
            print("File not found.\n")
            return

    datasets = load_transactions_from_file(filename)

    if datasets is None or len(datasets) == 0:
        print("No valid transaction data loaded.\n")
        return

    print(f"\nLoaded {len(datasets)} dataset(s).\n")

    for index, transactions in enumerate(datasets, start=1):

        print(f"\n========== DATASET {index} ==========")

        display_array("Original File Dataset:", transactions)

        print("\nRunning sorting algorithms...\n")

        m_time, m_sorted = time_algorithm(
            merge_sort,
            transactions.copy()
        )

        h_time, h_sorted = time_algorithm(
            heap_sort,
            transactions.copy()
        )

        display_array("Sorted File Dataset:", m_sorted)

        faster = get_faster(m_time, h_time)

        print("\nResults")
        print("-" * 40)
        print(f"Dataset Number: {index}")
        print(f"Dataset Size: {len(transactions)}")
        print(f"Merge Sort Time: {m_time:.8f}")
        print(f"Heap Sort Time:  {h_time:.8f}")
        print(f"Faster Algorithm: {faster}")

        if m_sorted == h_sorted:

            save_result(
                session_id,
                len(transactions),
                "file_input",
                m_time,
                h_time,
                faster
            )

            print("Result saved to database.\n")

# Loop of the main menu
def main():
    create_database()
    session_id = get_new_session_id()

    while True:
        print("\n--- Financial Sorting System ---")
        print(f"Session ID: {session_id}")
        print("1. Random Mixed Test")
        print("2. Custom Input")
        print("3. Load Input From File")
        print("4. View All Results")
        print("5. View Session Results")
        print("6. Complexity Info")
        print("7. Quit")

        choice = input("Choice: ")

        if choice == "1":
            run_random_test(session_id)
        elif choice == "2":
            run_custom_test(session_id)
        elif choice == "3":
            run_file_test(session_id)
        elif choice == "4":
            show_all_results()
        elif choice == "5":
            show_session_results()
        elif choice == "6":
            show_complexity()
        elif choice == "7":
            print("Exiting program.")
            break
        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()
