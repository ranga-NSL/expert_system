import pandas as pd
import graphviz
import openpyxl  # Ensure openpyxl is imported
file_path = "playbook_rules.xlsx"

# Load the Excel file into a DataFrame
df = pd.read_excel(file_path)

# Function to ask user about conditions
def check_conditions(df):
    current_id = 0  # Start with the first ID

    while current_id < len(df):
        condition = df.loc[current_id, 'Condition']
        action = df.loc[current_id, 'Action']
        response = input(f"{condition} (Yes/No or Y/N): ").strip().lower()

        if response in ['yes', 'y']:
            next_id = df.loc[current_id, 'Yes_Next_ID'] - 1  # Adjust for zero-based index
        elif response in ['no', 'n']:
            next_id = df.loc[current_id, 'No_Next_ID'] - 1  # Adjust for zero-based index
        else:
            print("Invalid response. Please answer with Yes/No or Y/N.")
            continue  # Skip to the next iteration

        # Check if the next ID is the same as the current ID
        if next_id == current_id:
            print(f"Action: {action}")
            print("Exiting the loop.")
            break  # Exit the loop if the next ID is the same as the current ID

        current_id = next_id  # Move to the next condition

    print("End of conditions.")

# Start checking conditions
check_conditions(df)