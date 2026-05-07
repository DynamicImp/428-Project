import sqlite3

DATABASE_NAME = "sorting_results.db"

# Creates database table
def create_database():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            input_size INTEGER,
            input_type TEXT,
            merge_time REAL,
            heap_time REAL,
            faster_algorithm TEXT,
            test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# Generates a new session ID
def get_new_session_id():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(session_id) FROM test_results")

    result = cursor.fetchone()[0]

    conn.close()

    if result is None:
        return 1

    return result + 1

# Saves sorting results to database
def save_result(session_id, size, input_type,
                merge_time, heap_time, faster):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO test_results
        (session_id, input_size, input_type,
         merge_time, heap_time, faster_algorithm)

        VALUES (?, ?, ?, ?, ?, ?)
    """, (session_id, size, input_type,
          merge_time, heap_time, faster))

    conn.commit()
    conn.close()

# Returns all database results
def view_all_results():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM test_results")

    rows = cursor.fetchall()

    conn.close()

    return rows

# Returns results for one session
def view_results_by_session(session_id):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM test_results
        WHERE session_id = ?
    """, (session_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows
