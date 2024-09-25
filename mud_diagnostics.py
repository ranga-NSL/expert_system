"""
Mud Diagnostics Application
----------------------------
This application is designed to diagnose issues related to mud properties in drilling operations.
It checks for symptoms such as changes in viscosity and density, applies relevant tests, and
generates hypotheses based on the observed symptoms.

Features:
- Check for symptoms and generate hypotheses
- Apply tests to determine the status of mud properties
- Display possible hypotheses based on symptoms and test results

Author: [Ranga Seshadri]
Date: [24-Sep-2024]
"""

import tkinter as tk
from tkinter import messagebox, ttk

class MudDiagnostics:
    # Constants for symptom changes and test statuses
    SYMPTOM_CHANGE_INCREASE = 'increase'
    SYMPTOM_CHANGE_DECREASE = 'decrease'
    TEST_STATUS_NIL = 'NIL'
    TEST_STATUS_READ = 'read'

    def __init__(self):
        self.symptoms = {
            'viscosity': {'change': self.SYMPTOM_CHANGE_INCREASE, 'degree': None},
            'density': {'change': self.SYMPTOM_CHANGE_DECREASE, 'degree': 'gradual'}
        }
        self.tests = {
            'MBT': {'for': 'low-SG-solids', 'status': self.TEST_STATUS_NIL},
            'oil-mud': {'for': 'unemulsified-water', 'status': self.TEST_STATUS_NIL}
        }
        self.hypotheses = {}

    def check_symptom(self, symptom_name: str) -> str:
        """Check the specified symptom and generate hypotheses."""
        symptom = self.symptoms.get(symptom_name)
        if symptom:
            if symptom['change'] == self.SYMPTOM_CHANGE_INCREASE:
                self.hypotheses['low-SG-solids'] = 'increase'
                self.hypotheses['unemulsified-water'] = 'increase'
                return f"Hypothesis: {symptom_name} increase"
            elif symptom['change'] == self.SYMPTOM_CHANGE_DECREASE:
                if symptom['degree'] == 'gradual':
                    self.hypotheses['shale'] = 'contamination'
                    return f"Hypothesis: {symptom_name} gradual decrease"
                elif symptom['degree'] == 'rapid':
                    self.hypotheses['water'] = 'influx'
                    return f"Hypothesis: {symptom_name} rapid decrease"
        return "No valid hypothesis found."

    def apply_tests(self) -> None:
        """Apply tests to determine the status of mud properties."""
        for name, test in self.tests.items():
            if test['status'] == self.TEST_STATUS_NIL:
                user_input = messagebox.askyesno("Test Confirmation", f"Is there {test['for']} according to the {name} test?")
                if user_input:
                    test['status'] = self.TEST_STATUS_READ
                    messagebox.showinfo("Test Result", f"Test {name} marked as read.")

    def show_hypotheses(self) -> str:
        """Display possible hypotheses based on symptoms and test results."""
        return "\n".join(f"{obj} {event} is a possibility" for obj, event in self.hypotheses.items())

class MudDiagnosticsGUI:
    def __init__(self, master):
        self.master = master
        master.title("Mud Diagnostics Application")

        self.diagnostics = MudDiagnostics()

        self.label = tk.Label(master, text="Select a symptom:")
        self.label.pack(pady=10)

        self.symptom_var = tk.StringVar()
        self.symptom_combobox = ttk.Combobox(master, textvariable=self.symptom_var, values=["viscosity", "density"])
        self.symptom_combobox.pack(pady=5)

        self.check_button = tk.Button(master, text="Check Symptom", command=self.check_symptom)
        self.check_button.pack(pady=5)

        self.result_label = tk.Label(master, text="", wraplength=300)
        self.result_label.pack(pady=10)

        self.hypotheses_button = tk.Button(master, text="Show Hypotheses", command=self.show_hypotheses)
        self.hypotheses_button.pack(pady=5)

    def check_symptom(self):
        symptom = self.symptom_var.get()
        if symptom:
            result = self.diagnostics.check_symptom(symptom)
            self.result_label.config(text=result)
            self.diagnostics.apply_tests()  # Apply tests after checking symptom
        else:
            messagebox.showerror("Input Error", "Please select a symptom.")

    def show_hypotheses(self):
        hypotheses = self.diagnostics.show_hypotheses()
        if hypotheses:
            messagebox.showinfo("Hypotheses", hypotheses)
        else:
            messagebox.showinfo("Hypotheses", "No hypotheses generated.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = MudDiagnosticsGUI(root)
    root.mainloop()