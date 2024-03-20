import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import matplotlib.pyplot as plt

# BMI Categories
BMI_CATEGORIES = {
    (0, 18.5): "Underweight",
    (18.5, 24.9): "Normal",
    (25, 29.9): "Overweight",
    (30, float('inf')): "Obese"
}

# GUI Setup
root = tk.Tk()
root.title("BMI Calculator")

# Functions
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        bmi = round(weight / (height * height), 2)
        category = classify_bmi(bmi)
        result_label.config(text=f"BMI: {bmi}, Category: {category}")
        save_data(weight, height, bmi)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid weight and height.")

def classify_bmi(bmi):
    for (lower, upper), category in BMI_CATEGORIES.items():
        if lower <= bmi < upper:
            return category

def save_data(weight, height, bmi):
    with open('bmi_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), weight, height, bmi])

def plot_bmi_trend():
    dates = []
    bmis = []
    with open('bmi_data.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            dates.append(row[0])
            bmis.append(float(row[3]))

    plt.figure(figsize=(10, 6))
    plt.plot(dates, bmis, marker='o')
    plt.xlabel('Date')
    plt.ylabel('BMI')
    plt.title('BMI Trend Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# GUI Components
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

# Run the GUI
root.mainloop()
