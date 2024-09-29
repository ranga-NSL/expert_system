"""
Wine Pairing Application
-------------------------
This application provides wine pairing recommendations based on selected dish types.
It utilizes a predefined set of wine pairing rules stored in a pandas DataFrame.
Users can select a dish type from a dropdown menu and receive suggestions for wine color,
body, flavor, and brand.

Features:
- User-friendly GUI built with Tkinter
- Combobox for dish selection
- Display of wine recommendations
- Exit functionality

Author: [Ranga Seshadri]
Date: [24-Sep-2024]

"""

import tkinter as tk
from tkinter import ttk
import pandas as pd

# Create a DataFrame for wine pairing rules
wine_pairing_rules = pd.DataFrame({
    'Dish Type': ['Paneer_Tikka', 'Dal_Makhani', 'Vegetable_Jalfrezi', 'Chole', 
                  'Vegetable_Biryani', 'Samosa', 'Chaat', 'Baingan_Bharta', 'Malai_Kofta'],
    'Wine Color': ['white', 'red', 'white', 'rosé', 'white', 'white', 'rosé', 'red', 'white'],
    'Wine Body': ['medium', 'full', 'off-dry', 'fruity', 'dry', 'crisp', 'fruity', 'light', 'semi-dry'],
    'Wine Flavor': ['smooth', 'spicy', 'aromatic', 'sparkling', 'aromatic', 'refreshing', 'sparkling', 'floral', 'buttery'],
    'Wine Brand': ['Chardonnay', 'Shiraz', 'Riesling', 'Prosecco', 'Sauvignon Blanc', 
                   'Sauvignon Blanc', 'Prosecco', 'Pinot Noir', 'Chardonnay']
})

# Create the main application window
root = tk.Tk()
root.title("Wine Pairing Recommendations")
root.geometry("400x300")  # Set a fixed size for the window

# Create a main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create a label for instructions
instruction_label = ttk.Label(main_frame, text="Select a dish type:")
instruction_label.grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky=tk.W)

# Create a combobox for dish types
dish_type_combobox = ttk.Combobox(main_frame, values=wine_pairing_rules['Dish Type'].tolist(), width=30)
dish_type_combobox.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)

# Create a label for recommendation caption
recommendation_caption = ttk.Label(main_frame, text="Recommendation:", font=("Arial", 10, "bold"))
recommendation_caption.grid(row=2, column=0, columnspan=2, pady=(10, 5), sticky=tk.W)

# Create a frame for recommendation display
recommendation_frame = ttk.Frame(main_frame, borderwidth=1, relief="solid", padding="5")
recommendation_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
main_frame.columnconfigure(1, weight=1)

# Create a label to display recommendations
recommendation_label = ttk.Label(recommendation_frame, text="", wraplength=350)
recommendation_label.pack(expand=True, fill=tk.BOTH)

# Function to get wine recommendation
def get_wine_recommendation():
    dish_type = dish_type_combobox.get().strip()  # Get the selected dish type
    print(f"Selected dish type: '{dish_type}'")  # Debugging output

    if not dish_type:
        recommendation_label.config(text="Please select a dish type.")
        return

    # Find the index of the selected dish type
    index = wine_pairing_rules[wine_pairing_rules['Dish Type'] == dish_type].index

    if not index.empty:
        # Get the corresponding wine attributes using the index
        wine_info = wine_pairing_rules.loc[index[0]]  # Get the first matching row
        recommendation = (
            f"Suggested wine for {dish_type}:\n"
            f"Color: {wine_info['Wine Color']}\n"
            f"Body: {wine_info['Wine Body']}\n"
            f"Flavor: {wine_info['Wine Flavor']}\n"
            f"Brand: {wine_info['Wine Brand']}"
        )
        recommendation_label.config(text=recommendation)
    else:
        recommendation_label.config(text=f"No wine pairing rule found for {dish_type}.")

# Create a button to get the wine recommendation
recommend_button = ttk.Button(main_frame, text="Get Recommendation", command=get_wine_recommendation)
recommend_button.grid(row=4, column=1, pady=(10, 0), padx=(5, 0), sticky=tk.E)

# Create an exit button
exit_button = ttk.Button(main_frame, text="Exit", command=root.quit)
exit_button.grid(row=5, column=1, pady=(5, 0), padx=(5, 0), sticky=tk.E)

# Run the application
root.mainloop()
