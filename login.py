import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import db
from main import open_app

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Login System")
root.geometry("400x300")

user_entry = ctk.CTkEntry(root, placeholder_text="Username")
user_entry.pack(pady=10)

pass_entry = ctk.CTkEntry(root, placeholder_text="Password", show="*")
pass_entry.pack(pady=10)


def login():
    conn = db.connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT role FROM users WHERE username=%s AND password=%s",
        (user_entry.get().strip(), pass_entry.get().strip())
    )

    result = cur.fetchone()
    conn.close()

    if result:
        root.destroy()
        open_app(result[0])
    else:
        messagebox.showerror("Login Failed", "Invalid Credentials")


ctk.CTkButton(root, text="Login", command=login).pack(pady=20)

root.mainloop()