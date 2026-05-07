from database import view_all_results
from database import view_results_by_session


# Displays all stored database results
def show_all_results():

    rows = view_all_results()

    if not rows:
        print("No results found.\n")
        return

    print("\nDatabase Results")
    print("-" * 90)

    for row in rows:
        print(row)

    print()


# Displays results from one session
def show_session_results():

    try:

        session_id = int(input("Enter session ID: "))

        rows = view_results_by_session(session_id)

        if not rows:
            print("No results for that session.\n")
            return

        print()

        for row in rows:
            print(row)

        print()

    except ValueError:
        print("Invalid session ID.\n")


# Displays complexity information
def show_complexity():

    print("\nAlgorithm Complexity")
    print("-" * 40)

    print("Merge Sort")
    print("Best Case:    O(n log n)")
    print("Average Case: O(n log n)")
    print("Worst Case:   O(n log n)")
    print("Space Complexity: O(n)\n")

    print("Heap Sort")
    print("Best Case:    O(n log n)")
    print("Average Case: O(n log n)")
    print("Worst Case:   O(n log n)")
    print("Space Complexity: O(1)\n")
