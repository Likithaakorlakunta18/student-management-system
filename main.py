from tkinter import messagebox
import matplotlib.pyplot as plt
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pandas as pd
import db

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def open_app(role):

    # ---------------- FUNCTIONS ---------------- #

    def refresh():
        conn = db.connect()
        cur = conn.cursor()

        # ✅ FIXED ORDER
        cur.execute("""
        SELECT id, name, age, course, phone, email, address, gender, dob
        FROM students
        """)

        rows = cur.fetchall()
        conn.close()

        table.delete(*table.get_children())

        for row in rows:
            table.insert("", tk.END, values=row)

    def clear():
        sid.set("")
        name.set("")
        age.set("")
        course.set("")
        phone.set("")
        email.set("")
        address.set("")
        gender.set("")
        dob.set("")

    def add_student():
        try:
            if name.get() == "" or age.get() == "" or course.get() == "":
                messagebox.showwarning("Warning", "Fill required fields")
                return

            conn = db.connect()
            cur = conn.cursor()

            cur.execute(
                """INSERT INTO students
                (name,age,course,phone,email,address,gender,dob)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    name.get(), age.get(), course.get(), phone.get(),
                    email.get(), address.get(), gender.get(), dob.get()
                )
            )

            conn.commit()
            conn.close()

            refresh()
            clear()
            messagebox.showinfo("Success", "Student Added")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_student():
        try:
            conn = db.connect()
            cur = conn.cursor()

            cur.execute("""
                UPDATE students
                SET name=%s, age=%s, course=%s, phone=%s,
                    email=%s, address=%s, gender=%s, dob=%s
                WHERE id=%s
            """, (
                name.get(), age.get(), course.get(), phone.get(),
                email.get(), address.get(), gender.get(), dob.get(),
                sid.get()
            ))

            conn.commit()
            conn.close()

            refresh()
            clear()
            messagebox.showinfo("Success", "Updated")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student():
        try:
            conn = db.connect()
            cur = conn.cursor()

            cur.execute("DELETE FROM students WHERE id=%s", (sid.get(),))

            conn.commit()
            conn.close()

            refresh()
            clear()
            messagebox.showinfo("Success", "Deleted")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def select_row(event):
        selected = table.focus()
        data = table.item(selected, "values")

        if data:
            sid.set(data[0])
            name.set(data[1])
            age.set(data[2])
            course.set(data[3])
            phone.set(data[4])
            email.set(data[5])
            address.set(data[6])
            gender.set(data[7])
            dob.set(data[8])

    def export_excel():
        conn = db.connect()
        cur = conn.cursor()

        # ✅ FIXED ORDER
        cur.execute("""
        SELECT id, name, age, course, phone, email, address, gender, dob
        FROM students
        """)

        rows = cur.fetchall()
        conn.close()

        df = pd.DataFrame(rows, columns=[
            "ID","Name","Age","Course","Phone","Email","Address","Gender","DOB"
        ])
        df.to_excel("students.xlsx", index=False)

        messagebox.showinfo("Success", "Excel Exported")

    def show_chart():
        conn = db.connect()
        cur = conn.cursor()

        cur.execute("SELECT course, COUNT(*) FROM students GROUP BY course")
        data = cur.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("Info", "No data")
            return

        courses = [x[0] for x in data]
        counts = [x[1] for x in data]

        plt.figure()
        plt.bar(courses, counts)
        plt.title("Students per Course")
        plt.xlabel("Course")
        plt.ylabel("Count")
        plt.show()

    # ---------------- WINDOW ---------------- #

    root = ctk.CTk()
    root.title("Student Management System")
    root.geometry("1200x700")

    ctk.CTkLabel(root, text="🎓 Dashboard", font=("Arial", 22)).pack(pady=10)

    container = ctk.CTkFrame(root)
    container.pack(fill="both", expand=True)

    sidebar = ctk.CTkFrame(container, width=200)
    sidebar.pack(side="left", fill="y")

    main = ctk.CTkFrame(container)
    main.pack(side="right", fill="both", expand=True)

    # ---------------- VARIABLES ---------------- #

    sid = tk.StringVar()
    name = tk.StringVar()
    age = tk.StringVar()
    course = tk.StringVar()
    phone = tk.StringVar()
    email = tk.StringVar()
    address = tk.StringVar()
    gender = tk.StringVar()
    dob = tk.StringVar()

    # ---------------- SIDEBAR ---------------- #

    add_btn = ctk.CTkButton(sidebar, text="Add", command=add_student)
    update_btn = ctk.CTkButton(sidebar, text="Update", command=update_student)
    delete_btn = ctk.CTkButton(sidebar, text="Delete", command=delete_student)

    add_btn.pack(pady=10, fill="x")
    update_btn.pack(pady=10, fill="x")
    delete_btn.pack(pady=10, fill="x")

    ctk.CTkButton(sidebar, text="Export", command=export_excel).pack(pady=10, fill="x")
    ctk.CTkButton(sidebar, text="Clear", command=clear).pack(pady=10, fill="x")
    ctk.CTkButton(sidebar, text="Chart", command=show_chart).pack(pady=10, fill="x")

    # Role restriction
    if role == "Student":
        update_btn.configure(state="disabled")
        delete_btn.configure(state="disabled")

    # ---------------- FORM ---------------- #

    labels = ["ID","Name","Age","Course","Phone","Email","Address","Gender","DOB"]
    variables = [sid, name, age, course, phone, email, address, gender, dob]

    for i in range(len(labels)):
        ctk.CTkLabel(main, text=labels[i]).grid(row=i//3, column=i%3, padx=10, pady=5)
        ctk.CTkEntry(main, textvariable=variables[i]).grid(row=i//3+1, column=i%3, padx=10, pady=5)

    # ---------------- TABLE ---------------- #

    table = ttk.Treeview(
        main,
        columns=("ID","Name","Age","Course","Phone","Email","Address","Gender","DOB"),
        show="headings"
    )

    for col in table["columns"]:
        table.heading(col, text=col)
        table.column(col, width=120)

    table.grid(row=5, column=0, columnspan=3, pady=20)

    table.bind("<ButtonRelease-1>", select_row)

    refresh()
    root.mainloop()