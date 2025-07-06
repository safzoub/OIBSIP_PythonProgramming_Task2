import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

def init_db():
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
                        username TEXT,
                        weight REAL,
                        height REAL,
                        bmi REAL,
                        date TEXT)''')
    conn.commit()
    conn.close()

def calculate_bmi(weight, height):
    if height <= 0:
        raise ValueError("Height must be greater than zero.")
    return round(weight / ((height / 100) ** 2), 2)

def store_bmi(username, weight, height, bmi):
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bmi_records VALUES (?, ?, ?, ?, ?)",
                   (username, weight, height, bmi, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def fetch_user_data(username):
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, bmi FROM bmi_records WHERE username = ?", (username,))
    data = cursor.fetchall()
    conn.close()
    return data

def plot_bmi(username):
    data = fetch_user_data(username)
    if not data:
        messagebox.showinfo("No Data", "No BMI records found for this user.")
        return
    dates, bmis = zip(*data)
    plt.plot(dates, bmis, marker='o')
    plt.title(f"{username}'s BMI Trend")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def on_calculate():
    try:
        username = name_entry.get().strip()
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        if not username:
            raise ValueError("Username is required.")
        bmi = calculate_bmi(weight, height)
        bmi_result_var.set(f"{bmi}")
        store_bmi(username, weight, height, bmi)
        messagebox.showinfo("Success", f"BMI for {username} recorded.")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

init_db()
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x300")
root.resizable(False, False)

ttk.Label(root, text="Username").grid(row=0, column=0, padx=10, pady=5, sticky="e")
name_entry = ttk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(root, text="Weight (kg)").grid(row=1, column=0, padx=10, pady=5, sticky="e")
weight_entry = ttk.Entry(root)
weight_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(root, text="Height (cm)").grid(row=2, column=0, padx=10, pady=5, sticky="e")
height_entry = ttk.Entry(root)
height_entry.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(root, text="BMI").grid(row=3, column=0, padx=10, pady=5, sticky="e")
bmi_result_var = tk.StringVar()
bmi_result = ttk.Label(root, textvariable=bmi_result_var)
bmi_result.grid(row=3, column=1, padx=10, pady=5)

ttk.Button(root, text="Calculate", command=on_calculate).grid(row=4, column=0, columnspan=2, pady=10)
ttk.Button(root, text="View Graph", command=lambda: plot_bmi(name_entry.get())).grid(row=5, column=0, columnspan=2)

root.mainloop()
