import random
import time

from heap_sort import heap_sort
from merge_sort import merge_sort
from database import create_database, get_new_session_id, save_result
from analysis import show_all_results, show_session_results, show_complexity

MAX_SIZE = 200000  # Maximum dataset size


# Generates a list of random values
def generate_transactions(size):
    return [round(random.uniform(1.0, 10000.0), 2) for _ in range(size)]


def display_array(title, arr, limit=20):
    print(f"\n{title}")
    if len(arr) <= limit:
        print(arr)
    else:
        print(arr[:limit])
        print(f"... showing first {limit} of {len(arr)} items")

def time_algorithm(func, data):
    start = time.perf_counter()
    result = func(data)
    end = time.perf_counter()
    return end - start, result

def get_faster(m_time, h_time):
    if m_time < h_time:
        return "Merge Sort"
    elif h_time < m_time:
        return "Heap Sort"
    return "Tie"

def run_random_test(session_id):
    
    size = random.randint(1, MAX_SIZE)

    
    transactions = generate_transactions(size)

    # Display original data (limited to 20 items)
    display_array("Original Transactions:", transactions)

    print("\nRunning sorting algorithms...\n")

    # Run Merge Sort
    m_time, m_sorted = time_algorithm(merge_sort, transactions.copy())

    # Run Heap Sort
    h_time, h_sorted = time_algorithm(heap_sort, transactions.copy())

    # Display sorted data
    display_array("Sorted Transactions:", m_sorted)

    # Determine faster algorithm
    faster = get_faster(m_time, h_time)

    print("\nResults")
    print("-" * 40)
    print(f"Size: {size}")
    print(f"Merge Sort Time: {m_time:.8f}")
    print(f"Heap Sort Time:  {h_time:.8f}")
    print(f"Faster Algorithm: {faster}")

    # Save results to database if sorting is correct
    if m_sorted == h_sorted:
        save_result(session_id, size, "random", m_time, h_time, faster)


# Runs a test using user-provided input
def run_custom_test(session_id):
    
    user_input = input("Enter integers separated by spaces: ")

    try:
        
        arr = list(map(int, user_input.split()))
    except:
        print("Invalid input.\n")
        return

    display_array("Original Array:", arr)

    print("\nRunning sorting algorithms...\n")

    m_time, m_sorted = time_algorithm(merge_sort, arr.copy())

    h_time, h_sorted = time_algorithm(heap_sort, arr.copy())

    display_array("Sorted Array:", m_sorted)

    faster = get_faster(m_time, h_time)

    print("\nResults")
    print("-" * 40)
    print(f"Size: {len(arr)}")
    print(f"Merge Sort Time: {m_time:.8f}")
    print(f"Heap Sort Time:  {h_time:.8f}")
    print(f"Faster Algorithm: {faster}")

    #Saves all results to database
    if m_sorted == h_sorted:
        save_result(session_id, len(arr), "custom", m_time, h_time, faster)


# Main menu of the loop
def main():
    #Initialize database
    create_database()

    #Creates a new session ID
    session_id = get_new_session_id()

    while True:
        print("\n--- Financial Sorting System ---")
        print("1. Random Test")
        print("2. Custom Input")
        print("3. View All Results")
        print("4. View Session Results")
        print("5. Complexity Info")
        print("6. Quit")

        choice = input("Choice: ")

        if choice == "1":
            run_random_test(session_id)
        elif choice == "2":
            run_custom_test(session_id)
        elif choice == "3":
            show_all_results()
        elif choice == "4":
            show_session_results()
        elif choice == "5":
            show_complexity()
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()