import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
import pandas as pd

# BMI Categories
BMI_CATEGORIES = {
    (0, 18.5): "Underweight",
    (18.5, 24.9): "Normal",
    (25, 29.9): "Overweight",
    (30, float('inf')): "Obese"
}

# Global variables
user_profiles = defaultdict(list)

# GUI Setup
root = tk.Tk()
root.title("Advanced BMI Calculator")

# Functions
def calculate_bmi():
    try:
        user_id = user_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        bmi = round(weight / (height * height), 2)
        category = classify_bmi(bmi)
        result_label.config(text=f"BMI: {bmi}, Category: {category}")
        save_data(user_id, weight, height, bmi)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid weight and height.")

def classify_bmi(bmi):
    for (lower, upper), category in BMI_CATEGORIES.items():
        if lower <= bmi < upper:
            return category

def save_data(user_id, weight, height, bmi):
    user_profiles[user_id].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), weight, height, bmi))
    with open('bmi_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), weight, height, bmi])

def plot_bmi_trend():
    user_id = user_entry.get()
    if user_id not in user_profiles:
        messagebox.showerror("Error", "User ID not found.")
        return

    df = pd.DataFrame(user_profiles[user_id], columns=['Date', 'Weight', 'Height', 'BMI'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['BMI'], marker='o')
    plt.xlabel('Date')
    plt.ylabel('BMI')
    plt.title(f'BMI Trend Over Time for User {user_id}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def analyze_bmi_data():
    user_id = user_entry.get()
    if user_id not in user_profiles:
        messagebox.showerror("Error", "User ID not found.")
        return

    df = pd.DataFrame(user_profiles[user_id], columns=['Date', 'Weight', 'Height', 'BMI'])
    category_counts = df['BMI'].apply(lambda x: classify_bmi(x)).value_counts()
    average_bmi = df['BMI'].mean()

    messagebox.showinfo("BMI Analysis", f"Average BMI: {average_bmi}\n\nBMI Category Counts:\n{category_counts}")

# GUI Components
user_label = tk.Label(root, text="User ID:")
user_label.pack()
user_entry = tk.Entry(root)
user_entry.pack()

weight_label = tk.Label(root, text="Weight (kg):")
weight_label.pack()
weight_entry = tk.Entry(root)
weight_entry.pack()

height_label = tk.Label(root, text="Height (m):")
height_label.pack()
height_entry = tk.Entry(root)
height_entry.pack()

calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi)
calculate_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

plot_button = tk.Button(root, text="Plot BMI Trend", command=plot_bmi_trend)
plot_button.pack()

analyze_button = tk.Button(root, text="Analyze BMI Data", command=analyze_bmi_data)
analyze_button.pack()

# Run the GUI
root.mainloop()
