# database_operations.py

import sqlite3

def connect_to_database(db_name="students.db"):
    return sqlite3.connect(db_name)

def create_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS students
                      (id INTEGER PRIMARY KEY, name TEXT, grade TEXT)''')

def insert_student(cursor, name, grade):
    cursor.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (name, grade))

def read_student(cursor, name):
    cursor.execute("SELECT * FROM students WHERE name=?", (name,))
    return cursor.fetchall()

def update_student_grade(cursor, name, grade):
    cursor.execute("UPDATE students SET grade=? WHERE name=?", (grade, name))

def delete_student(cursor, name):
    cursor.execute("DELETE FROM students WHERE name=?", (name,))

def count_students_by_grade(cursor, grade):
    cursor.execute("SELECT COUNT(*) FROM students WHERE grade=?", (grade,))
    return cursor.fetchone()

def fetch_students_ordered_by_name(cursor):
    cursor.execute("SELECT * FROM students ORDER BY name")
    return cursor.fetchall()

def main():
    conn = connect_to_database()
    cursor = conn.cursor()
    
    create_table(cursor)
    
    insert_student(cursor, "Alice", "A")
    print(read_student(cursor, "Alice"))

    update_student_grade(cursor, "Alice", "B")
    print(read_student(cursor, "Alice"))
    
    print(count_students_by_grade(cursor, "A"))
    
    print(fetch_students_ordered_by_name(cursor))
    
    delete_student(cursor, "Alice")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
