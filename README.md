# IDS706-Week7-miniProj-Command-Line-Tool
[![CI](https://github.com/Jingzhi-cyber/jz422-IDS706-Week7-CommmandLineTool/actions/workflows/cicd.yml/badge.svg)](https://github.com/Jingzhi-cyber/jz422-IDS706-Week7-CommmandLineTool/actions/workflows/cicd.yml)

This repository sets up an environment on CodeSpaces and uses GitHub Actions to run a Makefile for the following commands: make install, make test, make format, and make lint.

Packaging Python scripts into command-line tools can significantly enhance user experience and distribution. With the power of setuptools and careful structuring, you can turn even complex applications into user-friendly command-line tools.

## Getting Started
To set up the project, simply run make all or run make install and make test.

## Interact with SQLite database
A Python script designed to manage student and course data through interaction with an SQLite database, performing various SQL operations including creating tables, inserting data, and executing a complex SQL query.

## How to Use the Command-Line Tool
The `database_operations.py` script has been enhanced to function as a command-line tool, offering the following functionalities:

### Installation:

`pip3 install -e .`

![Alt text](install.png)

### Student Management:

- **Add a New Student by Name:** 
    - `mytool --add-student [NAME]`

- **List All Students:** 
    - `mytool --list-students`

- **Update a Student's Name by ID:** 
    - `mytool --update [ID] [NEW_NAME]`

- **Delete a Student by ID:** 
    - `mytool --delete [ID]`

- **Find Students by Name:** 
    - `mytool --find [NAME]`

### Course Management:

- **Add a Course for a Student by ID:** 
    - `mytool --add-course [STUDENT_ID] [COURSE_NAME] [SCORE]`

- **List All Courses for All Students:** 
    - `mytool --list-courses`

### Complex Query:

- **Execute Complex Query:** 
    - `mytool --complex-query`
    - This query retrieves the name and grade of each student, the number of courses they are enrolled in, and their average score.

### Sample Output:

![Alt text](output1.png)
![Alt text](output2.png)
![Alt text](output3.png)


## Database Schema
- **students**
    - **id**: INTEGER (PRIMARY KEY)
    - **name**: TEXT
    - **grade**: TEXT

- **courses**
    - **course_id**: INTEGER (PRIMARY KEY)
    - **student_id**: INTEGER (FOREIGN KEY, references id in students)
    - **course_name**: TEXT
    - **score**: INTEGER

## Complex Query Explanation
The script executes a complex SQL query to extract data about the students and their associated courses. Specifically, the query retrieves:

- The name and grade of each student.
- The number of courses each student is enrolled in.
- The average score of all courses per student.

### SQL Query

    SELECT s.name, s.grade, COUNT(c.course_id) AS num_courses, COALESCE(AVG(c.score), 0) AS avg_score
    FROM students s
    LEFT JOIN courses c ON s.id = c.student_id
    GROUP BY s.id, s.name, s.grade
    ORDER BY s.name

### Explanation
- **FROM students s**: Specifies that the student table is the main table.
- **LEFT JOIN courses c ON s.id = c.student_id**: Joins the student table with the courses table using a left join on the student ID. A left join is used to ensure that students without courses are still included in the results.
- **GROUP BY s.id, s.name, s.grade**: Groups the results by student, which aggregates course data per student.
- **COUNT(c.course_id) AS num_courses**: Counts the number of courses per student by counting course IDs in the aggregated data.
- **COALESCE(AVG(c.score), 0) AS avg_score**: Calculates the average score per student and replaces NULL with 0 if a student is not enrolled in any courses.
- **ORDER BY s.name**: Orders the results by student name to make the output user-friendly and orderly.

### Expected Results
The query will output a sorted list of students, each with their grade, total number of courses enrolled, and their average score across all courses. Even students not enrolled in any courses will be displayed, with 0 as both the number of courses and average score

## Project Structure
- **.devcontainer** includes a Dockerfile and devcontainer.json. The **Dockerfile** within this folder specifies how the container should be built, and other settings in this directory may control development environment configurations.
- **workflows** includes GitHub Actions, which contain configuration files for setting up automated build, test, and deployment pipelines for your project.
- **.gitignore** is used to specify which files or directories should be excluded from version control when using Git.
- **Makefile** is a configuration file used in Unix-based systems for automating tasks and building software. It contains instructions and dependencies for compiling code, running tests, and other development tasks.
- **README.md** is the instruction file for the readers.
- **requirements.txt** is to specify the dependencies (libraries and packages) required to run the project.
- **test_main.py** is a test file for main.py that can successfully run in IDEs.
- **main.py** is a Python file that contains the main function.
- **school.db** is a SQLite database file. It will be automatically generated after the first script execution and will store the students table along with its records.
- **setup.py** is a script for packaging the command-line tool.
- **mytool** is a directory containing the core scripts and modules.
    - `__init__.py` is an empty file required to treat directories as containing packages.
    - `database_operations.py` is the main Python script that contains functions to connect to the database, performing various SQL operations including creating tables, inserting data, and executing a complex SQL query.
