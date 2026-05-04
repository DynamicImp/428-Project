from database import view_all_results, view_results_by_session


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


def show_session_results():
    try:
        session_id = int(input("Enter session ID: "))
        rows = view_results_by_session(session_id)

        if not rows:
            print("No results for that session.\n")
            return

        for row in rows:
            print(row)

        print()

    except ValueError:
        print("Invalid session ID.\n")


def show_complexity():
    print("\nComplexity Analysis")
    print("-" * 40)

    print("Merge Sort: O(n log n)")
    print("Heap Sort:  O(n log n)\n")