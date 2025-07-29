# coding: utf-8
# @Author: bgtech
import sqlite3

def execute_query(query):
    conn = sqlite3.connect('your_database.db')  # Update with your database
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]