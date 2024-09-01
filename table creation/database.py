import sqlite3

def create_table():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER,
        grade TEXT
    )
    ''')
    conn.commit()
    conn.close()

def insert_student(first_name, last_name, age, grade):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO students (first_name, last_name, age, grade)
    VALUES (?, ?, ?, ?)
    ''', (first_name, last_name, age, grade))
    conn.commit()
    conn.close()

def fetch_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_student(student_id, first_name, last_name, age, grade):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE students
    SET first_name = ?, last_name = ?, age = ?, grade = ?
    WHERE id = ?
    ''', (first_name, last_name, age, grade, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM students
    WHERE id = ?
    ''', (student_id,))
    conn.commit()
    conn.close()