from collections import defaultdict


class State:
    def __init__(self, name: str):
        self.name = name
        self.is_final = False
        self.transitions = defaultdict(set)

    def add_transition(self, symbol: str, target_state: str):
        self.transitions[symbol].add(target_state)