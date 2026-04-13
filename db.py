import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",   # 🔴 change this
        database="student_db"
    )