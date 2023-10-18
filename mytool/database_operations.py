import argparse
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
    return cursor.lastrowid

def insert_course(cursor, student_id, course_name, score):
    cursor.execute(
        "INSERT INTO courses (student_id, course_name, score) VALUES (?, ?, ?)",
        (student_id, course_name, score),
    )

def list_students(cursor):
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()

def list_courses(cursor):
    cursor.execute("SELECT * FROM courses")
    return cursor.fetchall()

def update_student_name(cursor, student_id, new_name):
    cursor.execute("UPDATE students SET name=? WHERE id=?", (new_name, student_id))

def delete_student(cursor, student_id):
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))

def find_student_by_name(cursor, name):
    cursor.execute("SELECT * FROM students WHERE name=?", (name,))
    return cursor.fetchall()

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
    parser = argparse.ArgumentParser(description="Manage students and courses in a database.")
    
    parser.add_argument('--add', metavar='NAME', help='Add a new student by name')
    parser.add_argument('--list', action='store_true', help='List all students')
    parser.add_argument('--update', nargs=2, metavar=('ID', 'NEW_NAME'), help="Update a student's name by their ID")
    parser.add_argument('--delete', metavar='ID', help='Delete a student by their ID')
    parser.add_argument('--find', metavar='NAME', help='Find students by name')
    parser.add_argument('--add-course', nargs=3, metavar=('STUDENT_NAME', 'COURSE_NAME', 'SCORE'), help='Add a course for a student')
    parser.add_argument('--list-courses', action='store_true', help='List all courses for all students')
    parser.add_argument('--complex-query', action='store_true', help='Run the complex query and display results')

    args = parser.parse_args()

    conn = connect_to_database()
    cursor = conn.cursor()

    create_tables(cursor)

    if args.add:
        insert_student(cursor, args.add, "Unknown Grade")  # Assuming grade is unknown for simplicity
        print(f"Added student with name: {args.add}")
    elif args.list:
        students = list_students(cursor)
        for student in students:
            print(student)
    elif args.update:
        update_student_name(cursor, args.update[0], args.update[1])
        print(f"Updated student with ID {args.update[0]} to name {args.update[1]}")
    elif args.delete:
        delete_student(cursor, args.delete)
        print(f"Deleted student with ID {args.delete}")
    elif args.find:
        students = find_student_by_name(cursor, args.find)
        for student in students:
            print(student)
    elif args.add_course:
        insert_course(cursor, args.add_course[0], args.add_course[1], args.add_course[2])
        print(f"Added course {args.add_course[1]} for student ID {args.add_course[0]} with score {args.add_course[2]}")
    elif args.list_courses:
        courses = list_courses(cursor)
        for course in courses:
            print(course)
    elif args.complex_query:
        results = complex_query(cursor)
        for row in results:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]:.2f}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
