import json

class InferenceEngine:

    def __init__(self, fact_base, rule_file):
        self.fact_base = fact_base

        with open(rule_file) as f:
            self.rules = json.load(f)

        self.triggered_rules = []

    def run(self):

        new_fact_added = True

        while new_fact_added:
            new_fact_added = False

            for rule in self.rules:

                if rule["id"] in self.triggered_rules:
                    continue

                conditions_met = True

                for cond in rule["conditions"]:

                    fact_value = self.fact_base.get_fact(cond["fact"])

                    if fact_value != cond["value"]:
                        conditions_met = False
                        break

                if conditions_met:

                    conclusion = rule["conclusion"]

                    self.fact_base.add_fact(
                        conclusion["fact"],
                        conclusion["value"]
                    )

                    self.triggered_rules.append(rule["id"])

                    new_fact_added = True
