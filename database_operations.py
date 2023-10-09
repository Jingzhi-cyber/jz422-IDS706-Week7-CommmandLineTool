import sqlite3

def connect_to_database(db_name="school.db"):
    return sqlite3.connect(db_name)


def create_tables(cursor):
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS students
           (id INTEGER PRIMARY KEY, name TEXT, grade TEXT)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS courses
           (course_id INTEGER PRIMARY KEY, student_id INTEGER,
            course_name TEXT, score INTEGER,
            FOREIGN KEY (student_id) REFERENCES students (id))"""
    )


def insert_student(cursor, name, grade):
    cursor.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (name, grade))
    return cursor.lastrowid  # Returning the id of the inserted student


def insert_course(cursor, student_id, course_name, score):
    cursor.execute(
        "INSERT INTO courses (student_id, course_name, score) VALUES (?, ?, ?)",
        (student_id, course_name, score),
    )


def complex_query(cursor):
    cursor.execute(
        """SELECT s.name, s.grade, COUNT(c.course_id) AS num_courses, COALESCE(AVG(c.score), 0) AS avg_score
           FROM students s
           LEFT JOIN courses c ON s.id = c.student_id
           GROUP BY s.id, s.name, s.grade
           ORDER BY s.name"""
    )
    return cursor.fetchall()



def main():
    conn = connect_to_database()
    cursor = conn.cursor()

    create_tables(cursor)

    alice_id = insert_student(cursor, "Alice", "A")
    insert_course(cursor, alice_id, "Math", 90)
    insert_course(cursor, alice_id, "Physics", 85)
    
    bob_id = insert_student(cursor, "Bob", "B")
    insert_course(cursor, bob_id, "Math", 88)
    
    charlie_id = insert_student(cursor, "Charlie", "C")
    insert_course(cursor, charlie_id, "History", 92)
    insert_course(cursor, charlie_id, "Biology", 78)
    
    conn.commit()
    
    results = complex_query(cursor)
    print("Name | Grade | Number of Courses | Average Score")
    for row in results:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]:.2f}")
    
    conn.close()



if __name__ == "__main__":
    main()
