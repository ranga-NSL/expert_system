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

# Create a label for instructions
instruction_label = tk.Label(root, text="Select a dish type:")
instruction_label.pack(pady=10)

# Create a combobox for dish types
dish_type_combobox = ttk.Combobox(root, values=wine_pairing_rules['Dish Type'].tolist())
dish_type_combobox.pack(pady=5)

# Create a label to display recommendations
recommendation_label = tk.Label(root, text="", wraplength=300)
recommendation_label.pack(pady=10)

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
            f"Suggested wine for {dish_type}: "
            f"Color: {wine_info['Wine Color']}, "
            f"Body: {wine_info['Wine Body']}, "
            f"Flavor: {wine_info['Wine Flavor']}, "
            f"Brand: {wine_info['Wine Brand']}"
        )
        recommendation_label.config(text=recommendation)
    else:
        recommendation_label.config(text=f"No wine pairing rule found for {dish_type}.")

# Create a button to get the wine recommendation
recommend_button = tk.Button(root, text="Get Recommendation", command=get_wine_recommendation)
recommend_button.pack(pady=5)

# Create an exit button
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=5)

# Run the application
root.mainloop()
