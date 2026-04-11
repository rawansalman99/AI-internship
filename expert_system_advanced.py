import tkinter as tk  # Import Tkinter library for GUI to create windows and buttons
from tkinter import messagebox  # Import messagebox for popup alerts


# Rule Class

class Rule:
    def __init__(self, conditions, conclusion): #Constructor to run when create a rule
        self.conditions = conditions  # store list of conditions (IF part of rule)
        self.conclusion = conclusion  # store result (THEN part of rule)


# Expert System Class :main brain of the system

class ExpertSystem:
    def __init__(self): #initialize system when created
        self.facts = set()  # store known facts (no duplicates)
        self.rules = []  # store all rules in a list
        self.log = []  # store reasoning steps (inference log)

    def add_fact(self, fact): #function to add a fact
        self.facts.add(fact)  # add a new fact to the system

    def add_rule(self, rule):
        self.rules.append(rule)  # add a rule to the system

    def forward_chaining(self):#AI brain
        applied = True  # control variable to keep looping, keep system running until new fact appears

        while applied:  # keep running until no new rules apply
            applied = False  # assume no rule will apply

            for rule in self.rules:  # loop through all rules
                # check if ALL conditions of the rule exist in facts
                if all(cond in self.facts for cond in rule.conditions):
                    
                    # check if conclusion is not already known
                    if rule.conclusion not in self.facts:
                        
                        self.facts.add(rule.conclusion)  # Add new inferred fact
                        
                        # save reasoning step in log
                        self.log.append(
                            f"Applied: IF {rule.conditions} THEN {rule.conclusion}"
                        )
                        
                        applied = True  # a rule was applied → continue loop


# GUI Function

def run_system():
    system = ExpertSystem()  # Create a new expert system instance

    # Add rules (knowledge base)
    system.add_rule(Rule(["fever", "cough"], "flu"))  # IF fever AND cough → flu
    system.add_rule(Rule(["flu"], "rest"))  # IF flu → rest
    system.add_rule(Rule(["headache"], "painkiller"))  # IF headache → painkiller
    system.add_rule(Rule(["flu", "painkiller"], "recovering"))  # Multi-step rule

    user_input = entry.get()  # get text from input field (GUI)

    # check if input is empty
    if not user_input:
        messagebox.showwarning("Input Error", "Please enter symptoms")  # show popup
        return  # stop function execution

    symptoms = user_input.split(",")  # split input into list using comma

    # add each symptom as a fact
    for s in symptoms:
        system.add_fact(s.strip().lower())  # remove spaces + convert to lowercase

    system.forward_chaining()  # run inference engine (AI reasoning)

    output_text.delete(1.0, tk.END)  # clear previous results in output box

    output_text.insert(tk.END, "Inference Steps:\n")  # title for log

    # display all reasoning steps
    for step in system.log:
        output_text.insert(tk.END, step + "\n")

    output_text.insert(tk.END, "\nFinal Facts:\n")  # title for results

    # display all final facts (initial + inferred)
    for fact in system.facts:
        output_text.insert(tk.END, fact + "\n")


# GUI DESIGN

root = tk.Tk()  # create main window
root.title("Expert System")  # set window title
root.geometry("500x400")  # set window size

# create label (instruction text)
label = tk.Label(root, text="Enter symptoms (comma separated):")
label.pack(pady=10)  # Add spacing and place in window

# create input field
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# create button that runs the system
button = tk.Button(root, text="Run Expert System", command=run_system)
button.pack(pady=10)

# create text area to display results
output_text = tk.Text(root, height=15, width=60)
output_text.pack(pady=10)

root.mainloop()  # keep window running and wait for user interaction
