import openpyxl
from graphviz import Digraph

def read_excel_data(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        id, question, action, yes_next, no_next = row[:5]
        
        data.append({
            'id': id,
            'question': question,
            'action': action,
            'yes_next': yes_next if yes_next != id else None,
            'no_next': no_next if no_next != id else None
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
    excel_file = 'decision_tree_data.xlsx'
    output_file = 'decision_tree'

    data = read_excel_data(excel_file)
    decision_tree = create_decision_tree(data)
    decision_tree.render(output_file, format='png', cleanup=True)
    print(f"Decision tree has been generated and saved as {output_file}.png")

if __name__ == '__main__':
    main()
