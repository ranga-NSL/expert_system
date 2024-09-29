import pandas as pd
from graphviz import Digraph

def create_example_dataframe():
    data = {
        'ID': [1, 2, 3],
        'Question': ['Is it raining?', 'Is the sun shining?', 'End of decision tree'],
        'Action': ['Take an umbrella', 'Take a hat', 'Exit'],
        'Yes Next': [1, 2, 3],
        'No Next': [2, 3, 3]
    }
    return pd.DataFrame(data)

def process_dataframe(df):
    data = []
    for _, row in df.iterrows():
        data.append({
            'id': row['ID'],
            'question': row['Question'],
            'action': row['Action'],
            'yes_next': row['Yes Next'] if row['Yes Next'] != row['ID'] else None,
            'no_next': row['No Next'] if row['No Next'] != row['ID'] else None
        })
    return data

def create_decision_tree(data):
    dot = Digraph(comment='Decision Tree')
    dot.attr(rankdir='TB', size='8,8')

    for item in data:
        # Create question node
        dot.node(str(item['id']), item['question'], shape='diamond')
        
        # Create action node
        action_id = f"{item['id']}_action"
        dot.node(action_id, item['action'], shape='rectangle')
        
        # Connect question to action for 'Yes' if yes_next is None
        if item['yes_next'] is None:
            dot.edge(str(item['id']), action_id, label='Yes')
        else:
            dot.edge(str(item['id']), str(item['yes_next']), label='Yes')
        
        # Connect question to action for 'No' if no_next is None
        if item['no_next'] is None:
            dot.edge(str(item['id']), action_id, label='No')
        else:
            dot.edge(str(item['id']), str(item['no_next']), label='No')

    return dot

def main():
    # Comment out the Excel file reading
    # excel_file = 'decision_tree_data.xlsx'
    output_file = 'decision_tree'

    # Create example DataFrame
    df = create_example_dataframe()
    
    # Process the DataFrame
    data = process_dataframe(df)
    
    # Create and render the decision tree
    decision_tree = create_decision_tree(data)
    decision_tree.render(output_file, format='png', cleanup=True)
    print(f"Decision tree has been generated and saved as {output_file}.png")

if __name__ == '__main__':
    main()