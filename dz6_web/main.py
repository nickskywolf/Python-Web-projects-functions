from faker import Faker
import sqlite3
import random
from datetime import datetime, timedelta

fake = Faker()

# З'єднання з базою даних
conn = sqlite3.connect("university.db")
cursor = conn.cursor()

# Створення таблиць
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        group_id INTEGER
    );
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    );
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    );
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        teacher_id INTEGER
    );
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        grade INTEGER,
        date TEXT
    );
"""
)

# Заповнення таблиць випадковими даними
groups = ["Group A", "Group B", "Group C"]
for group in groups:
    cursor.execute("INSERT INTO groups (name) VALUES (?);", (group,))

teachers = ["Teacher 1", "Teacher 2", "Teacher 3"]
for teacher in teachers:
    cursor.execute("INSERT INTO teachers (name) VALUES (?);", (teacher,))

subjects = ["Math", "Physics", "Chemistry", "Biology", "History"]
for subject in subjects:
    teacher_id = random.randint(1, len(teachers))
    cursor.execute(
        "INSERT INTO subjects (name, teacher_id) VALUES (?, ?);", (subject, teacher_id)
    )

students_count = 50
for _ in range(students_count):
    name = fake.name()
    group_id = random.randint(1, len(groups))
    cursor.execute(
        "INSERT INTO students (name, group_id) VALUES (?, ?);", (name, group_id)
    )

grades_count = 100
for _ in range(grades_count):
    student_id = random.randint(1, students_count)
    subject_id = random.randint(1, len(subjects))
    grade = random.randint(60, 100)
    date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime(
        "%Y-%m-%d"
    )
    cursor.execute(
        "INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?);",
        (student_id, subject_id, grade, date),
    )

# Збереження змін у базі даних
conn.commit()

# Виконання SQL запитів та запис їх у файли
queries = [
    "SELECT students.name, AVG(grades.grade) as avg_grade FROM students "
    "JOIN grades ON students.id = grades.student_id "
    "GROUP BY students.id "
    "ORDER BY avg_grade DESC LIMIT 5;",
    "SELECT students.name, AVG(grades.grade) as avg_grade FROM students "
    "JOIN grades ON students.id = grades.student_id "
    "WHERE grades.subject_id = 1 "
    "GROUP BY students.id "
    "ORDER BY avg_grade DESC LIMIT 1;",
    "SELECT groups.name, AVG(grades.grade) as avg_grade FROM students "
    "JOIN groups ON students.group_id = groups.id "
    "JOIN grades ON students.id = grades.student_id "
    "WHERE grades.subject_id = 1 "
    "GROUP BY groups.id;",
    "SELECT AVG(grades.grade) as avg_grade FROM grades;",
    "SELECT subjects.name FROM subjects "
    "JOIN teachers ON subjects.teacher_id = teachers.id "
    "WHERE teachers.name = 'Teacher 1';",
    "SELECT students.name FROM students "
    "JOIN groups ON students.group_id = groups.id "
    "WHERE groups.name = 'Group A';",
    "SELECT grades.grade FROM grades "
    "JOIN students ON grades.student_id = students.id "
    "JOIN groups ON students.group_id = groups.id "
    "WHERE groups.name = 'Group A' AND grades.subject_id = 1;",
    "SELECT AVG(grades.grade) as avg_grade FROM grades "
    "JOIN subjects ON grades.subject_id = subjects.id "
    "JOIN teachers ON subjects.teacher_id = teachers.id "
    "WHERE teachers.name = 'Teacher 1';",
    "SELECT subjects.name FROM subjects "
    "JOIN grades ON subjects.id = grades.subject_id "
    "JOIN students ON grades.student_id = students.id "
    "WHERE students.name = 'John Doe';",
    "SELECT subjects.name FROM subjects "
    "JOIN grades ON subjects.id = grades.subject_id "
    "JOIN teachers ON subjects.teacher_id = teachers.id "
    "JOIN students ON grades.student_id = students.id "
    "WHERE students.name = 'John Doe' AND teachers.name = 'Teacher 1';",
]

for i, query in enumerate(queries, 1):
    with open(f"query_{i}.sql", "w") as file:
        file.write(query)

# Закриття з'єднання з базою даних
conn.close()
