"""
Decision Tree Navigator

This program implements an interactive decision tree navigator with a graphical user interface.
It reads decision tree data from an Excel file and guides the user through a series of
questions, visualizing the decision path as a tree diagram.

Features:
- Reads decision tree structure from an Excel file
- Provides a command-line interface for user input
- Dynamically updates and displays the decision tree diagram
- Uses Tkinter for the graphical user interface
- Utilizes Graphviz for generating the decision tree visualization

Dependencies:
- pandas: For reading the Excel file
- graphviz: For generating the decision tree diagram
- openpyxl: For Excel file support with pandas
- Pillow (PIL): For image processing
- tkinter: For the graphical user interface

Usage:
1. Ensure all dependencies are installed
2. Prepare an Excel file with the decision tree structure
3. Update the Excel file path in the main() function
4. Run the script

Author: [Ranga Seshadri]
Date: [2024-09-25]
Version: 1.0
"""

import pandas as pd
import graphviz
import openpyxl  # Ensure openpyxl is imported
import tkinter as tk  # Import tkinter for GUI
from tkinter import messagebox  # Import messagebox for alerts
from PIL import Image, ImageTk  # Import PIL for image handling
file_path = "playbook_rules.xlsx"

# Load the Excel file into a DataFrame
df = pd.read_excel(file_path)
# Function to plot the decision tree
def plot_decision_tree(path):
    dot = graphviz.Digraph()
    for i, (condition, response, action) in enumerate(path):
        dot.node(f'C{i}', condition)
        if action:
            dot.node(f'A{i}', action)
            dot.edge(f'C{i}', f'A{i}', label=response)
        if i > 0:
            dot.edge(f'C{i-1}', f'C{i}', label=path[i-1][1])
    
    dot.render('decision_tree', format='png', cleanup=False)

    window = tk.Toplevel()
    window.title("Decision Tree")
    img = Image.open('decision_tree.png')
    img = ImageTk.PhotoImage(img)
    label = tk.Label(window, image=img)
    label.image = img  # Keep a reference to avoid garbage collection
    label.pack()

# Function to ask user about conditions
def check_conditions(df, tree_gui):
    current_id = 0  # Start with the first ID
    path = []

    while current_id < len(df):
        condition = df.loc[current_id, 'Condition']
        action = df.loc[current_id, 'Action']
        
        response = input(f"{condition} (Yes/No or Y/N): ").strip().lower()

        if response in ['yes', 'y']:
            next_id = df.loc[current_id, 'Yes_Next_ID'] - 1
            response = 'Yes'
        elif response in ['no', 'n']:
            next_id = df.loc[current_id, 'No_Next_ID'] - 1
            response = 'No'
        else:
            print("Invalid response. Please answer with Yes/No or Y/N.")
            continue

        path.append((condition, response, action if next_id == current_id else None))
        tree_gui.update_tree(path)

        if next_id == current_id:
            print(f"Action: {action}")
            print("Exiting the loop.")
            break

        current_id = next_id

    print("End of conditions.")

class DecisionTreeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Decision Tree")
        self.canvas = tk.Canvas(self.master, width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.image_on_canvas = None

    def update_tree(self, path):
        dot = graphviz.Digraph()
        for i, (condition, response, action) in enumerate(path):
            dot.node(f'C{i}', condition)
            if action:
                dot.node(f'A{i}', action)
                dot.edge(f'C{i}', f'A{i}', label=response)
            if i > 0:
                dot.edge(f'C{i-1}', f'C{i}', label=path[i-1][1])
        
        dot.render('decision_tree', format='png', cleanup=True)

        img = Image.open('decision_tree.png')
        img = ImageTk.PhotoImage(img)
        
        self.canvas.delete("all")
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img
        self.master.update()

def main():
    # Load your DataFrame
    df = pd.read_excel(file_path)  # Replace with your actual file path

    # Initialize Tkinter root window
    root = tk.Tk()
    tree_gui = DecisionTreeGUI(root)

    # Start checking conditions
    check_conditions(df, tree_gui)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()