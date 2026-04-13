import tkinter as tk
from tkinter import messagebox
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="student_db"
)
cursor = conn.cursor()

def add_student():
    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (%s, %s, %s)",
        (name_entry.get(), age_entry.get(), course_entry.get())
    )
    conn.commit()
    messagebox.showinfo("Success", "Added")

def view_students():
    cursor.execute("SELECT * FROM students")
    output.delete(1.0, tk.END)
    for row in cursor.fetchall():
        output.insert(tk.END, str(row) + "\n")

def update_student():
    cursor.execute(
        "UPDATE students SET name=%s, age=%s, course=%s WHERE id=%s",
        (name_entry.get(), age_entry.get(), course_entry.get(), id_entry.get())
    )
    conn.commit()
    messagebox.showinfo("Success", "Updated")

def delete_student():
    cursor.execute(
        "DELETE FROM students WHERE id=%s",
        (id_entry.get(),)
    )
    conn.commit()
    messagebox.showinfo("Success", "Deleted")

root = tk.Tk()
root.title("Student Management System")

tk.Label(root, text="ID").grid(row=0, column=0)
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1)

tk.Label(root, text="Name").grid(row=1, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)

tk.Label(root, text="Age").grid(row=2, column=0)
age_entry = tk.Entry(root)
age_entry.grid(row=2, column=1)

tk.Label(root, text="Course").grid(row=3, column=0)
course_entry = tk.Entry(root)
course_entry.grid(row=3, column=1)

tk.Button(root, text="Add", command=add_student).grid(row=4, column=0)
tk.Button(root, text="View", command=view_students).grid(row=4, column=1)
tk.Button(root, text="Update", command=update_student).grid(row=5, column=0)
tk.Button(root, text="Delete", command=delete_student).grid(row=5, column=1)

output = tk.Text(root, height=10, width=40)
output.grid(row=6, column=0, columnspan=2)

root.mainloop()