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