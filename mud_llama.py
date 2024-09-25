import tkinter as tk
from tkinter import messagebox, ttk

class MudDiagnostics:
    SYMPTOM_CHANGE_INCREASE = 'increase'
    SYMPTOM_CHANGE_DECREASE = 'decrease'
    TEST_STATUS_NIL = 'NIL'
    TEST_STATUS_READ = 'read'

    def __init__(self):
        self.symptoms = {
            'viscosity': {'change': self.SYMPTOM_CHANGE_INCREASE},
            'density': {'change': self.SYMPTOM_CHANGE_DECREASE, 'degree': 'gradual'}
        }
        self.tests = {
            'SGT': {'status': self.TEST_STATUS_NIL, 'for': 'low-SG-solids'},
            'URT': {'status': self.TEST_STATUS_NIL, 'for': 'unemulsified-water'},
            'SWC': {'status': self.TEST_STATUS_NIL, 'for': 'shale'}
        }
        self.hypotheses = {}

    def check_symptom(self, symptom_name):
        symptom = self.symptoms.get(symptom_name)
        if symptom:
            if symptom['change'] == self.SYMPTOM_CHANGE_INCREASE:
                self.hypotheses['low-SG-solids'] = 'increased'
                self.hypotheses['unemulsified-water'] = 'increased'
            elif symptom['change'] == self.SYMPTOM_CHANGE_DECREASE:
                if symptom.get('degree', 'rapid') == 'gradual':
                    self.hypotheses['shale'] = 'contamination'
                elif symptom['degree'] == 'rapid':
                    self.hypotheses['water'] = 'influx'
            return f"Symptom {symptom_name} has resulted in the following hypotheses: {', '.join(self.hypotheses.values())}"
        else:
            return "No valid symptoms found."

    def apply_tests(self):
        for name, test in self.tests.items():
            if test['status'] == self.TEST_STATUS_NIL:
                user_input = messagebox.askyesno("Test Confirmation", 
                    f"Is there {test['for']} according to the {name} test?")
                if user_input:
                    test['status'] = self.TEST_STATUS_READ
                    messagebox.showinfo("Test Result", f"Test {name} marked as read.")

    def show_hypotheses(self):
        return "\n".join(f"{obj}: {event}" for obj, event in self.hypotheses.items())

class MudDiagnosticsGUI:
    def __init__(self, master):
        self.master = master
        master.title("Mud Diagnostics Application")

        self.diagnostics = MudDiagnostics()

        self.label = tk.Label(master, text="Select a symptom:")
        self.label.pack(pady=10)

        self.symptom_var = tk.StringVar()
        self.symptom_combobox = ttk.Combobox(master, textvariable=self.symptom_var, values=["viscosity",
"density"])
        self.symptom_combobox.pack(pady=5)

        self.check_button = tk.Button(master, text="Check Symptom", command=self.check_symptom)
        self.check_button.pack(pady=5)

        self.result_label = tk.Label(master, text="", wraplength=300)
        self.result_label.pack(pady=10)

        self.hypotheses_button = tk.Button(master, text="Show Hypotheses", command=self.show_hypotheses)
        self.hypotheses_button.pack(pady=5)

    def check_symptom(self):
        symptom = self.symptom_var.get()
        result = self.diagnostics.check_symptom(symptom)
        self.result_label.config(text=result)
        self.diagnostics.apply_tests()

    def show_hypotheses(self):
        hypotheses = self.diagnostics.show_hypotheses()
        messagebox.showinfo("Hypotheses", hypotheses)

if __name__ == "__main__":
    root = tk.Tk()
    gui = MudDiagnosticsGUI(root)
    root.mainloop()
