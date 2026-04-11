# Rule-Based Expert System with Forward Chaining

class Rule:
    def __init__(self, conditions, conclusion):
        self.conditions = conditions  # list of conditions
        self.conclusion = conclusion  # result

class ExpertSystem:
    def __init__(self):
        self.facts = set()
        self.rules = []
        self.log = []

    def add_fact(self, fact):
        self.facts.add(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

    def forward_chaining(self):
        applied = True

        while applied:
            applied = False

            for rule in self.rules:
                # Check if rule conditions are satisfied
                if all(cond in self.facts for cond in rule.conditions):
                    if rule.conclusion not in self.facts:
                        self.facts.add(rule.conclusion)
                        self.log.append(
                            f"Applied rule: IF {rule.conditions} THEN {rule.conclusion}"
                        )
                        applied = True

    def show_log(self):
        print("\nInference Steps:")
        for step in self.log:
            print(step)

    def show_facts(self):
        print("\nFinal Facts:")
        for fact in self.facts:
            print(fact)


# ==========================
# MAIN PROGRAM
# ==========================

system = ExpertSystem()

# Define rules
system.add_rule(Rule(["fever", "cough"], "flu"))
system.add_rule(Rule(["flu"], "rest"))
system.add_rule(Rule(["headache"], "painkiller"))
system.add_rule(Rule(["flu", "painkiller"], "recovering"))

# Get user input
print("Enter symptoms (comma separated): ")
user_input = input()

symptoms = user_input.split(",")

for s in symptoms:
    system.add_fact(s.strip())

# Run inference
system.forward_chaining()

# Show results
system.show_log()
system.show_facts()