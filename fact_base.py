class FactBase:
    def __init__(self):
        self.facts = {}

    def add_fact(self, fact, value):
        self.facts[fact] = value

    def get_fact(self, fact):
        return self.facts.get(fact, None)

    def has_fact(self, fact):
        return fact in self.facts
