import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Function to add a new student
def add_student():
    name = entry_name.get()
    age = entry_age.get()
    grade = entry_grade.get()
    course = entry_course.get()

    if name and age and grade and course:
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO students (name, age, grade, course)
        VALUES (?, ?, ?, ?)
        ''', (name, age, grade, course))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_entries()
        refresh_students()
    else:
        messagebox.showwarning("Input Error", "All fields are required.")

# Function to update a student
def update_student():
    selected = students_treeview.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a student to update.")
        return

    index = selected[0]
    student_id = students_treeview.item(index)['values'][0]
    name = entry_name.get()
    age = entry_age.get()
    grade = entry_grade.get()
    course = entry_course.get()

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE students
    SET name = ?, age = ?, grade = ?, course = ?
    WHERE id = ?
    ''', (name, age, grade, course, student_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student updated successfully!")
    clear_entries()
    refresh_students()

# Function to delete a student
def delete_student():
    selected = students_treeview.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a student to delete.")
        return

    index = selected[0]
    student_id = students_treeview.item(index)['values'][0]

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student deleted successfully!")
    clear_entries()
    refresh_students()

# Function to search for students
def search_students():
    query = entry_search.get()
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM students
    WHERE name LIKE ? OR course LIKE ?
    ''', (f'%{query}%', f'%{query}%'))
    rows = cursor.fetchall()
    conn.close()
    display_students(rows)

# Function to refresh the students list
def refresh_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    conn.close()
    display_students(rows)

# Function to display students in the treeview
def display_students(rows):
    for row in students_treeview.get_children():
        students_treeview.delete(row)
    for row in rows:
        students_treeview.insert('', tk.END, values=row)

# Function to clear input fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_grade.delete(0, tk.END)
    entry_course.delete(0, tk.END)

# Function to populate input fields with selected student
def populate_fields(event):
    selected = students_treeview.selection()
    if selected:
        index = selected[0]
        values = students_treeview.item(index)['values']
        entry_name.delete(0, tk.END)
        entry_name.insert(tk.END, values[1])
        entry_age.delete(0, tk.END)
        entry_age.insert(tk.END, values[2])
        entry_grade.delete(0, tk.END)
        entry_grade.insert(tk.END, values[3])
        entry_course.delete(0, tk.END)
        entry_course.insert(tk.END, values[4])

# Create the main Tkinter window
root = tk.Tk()
root.title("Student Management System")

# Create input fields and labels
label_name = tk.Label(root, text="Name")
label_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=5, pady=5)

label_age = tk.Label(root, text="Age")
label_age.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry_age = tk.Entry(root)
entry_age.grid(row=1, column=1, padx=5, pady=5)

label_grade = tk.Label(root, text="Grade")
label_grade.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
entry_grade = tk.Entry(root)
entry_grade.grid(row=2, column=1, padx=5, pady=5)

label_course = tk.Label(root, text="Course")
label_course.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
entry_course = tk.Entry(root)
entry_course.grid(row=3, column=1, padx=5, pady=5)

# Create buttons for operations
button_add = tk.Button(root, text="Add Student", command=add_student)
button_add.grid(row=4, column=0, columnspan=2, pady=5)

button_update = tk.Button(root, text="Update Student", command=update_student)
button_update.grid(row=5, column=0, columnspan=2, pady=5)

button_delete = tk.Button(root, text="Delete Student", command=delete_student)
button_delete.grid(row=6, column=0, columnspan=2, pady=5)

# Create search field and button
entry_search = tk.Entry(root)
entry_search.grid(row=7, column=0, padx=5, pady=5)

button_search = tk.Button(root, text="Search", command=search_students)
button_search.grid(row=7, column=1, pady=5)

# Create treeview to display students
columns = ('ID', 'Name', 'Age', 'Grade', 'Course')
students_treeview = ttk.Treeview(root, columns=columns, show='headings')
students_treeview.heading('ID', text='ID')
students_treeview.heading('Name', text='Name')
students_treeview.heading('Age', text='Age')
students_treeview.heading('Grade', text='Grade')
students_treeview.heading('Course', text='Course')
students_treeview.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
students_treeview.bind('<<TreeviewSelect>>', populate_fields)

# Initialize student list
refresh_students()

# Run the Tkinter event loop
root.mainloop()