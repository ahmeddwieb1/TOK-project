from State import State


class Automaton:
    def __init__(self):
        self.states = {}  # name -> State object
        self.start_state = None
        self.final_states = set()
        self.alphabet = set()

    def add_state(self, name: str) -> State:
        if name not in self.states:
            self.states[name] = State(name)
        return self.states[name]

    def add_transition(self, from_state: str, to_state: str, symbol: str):
        self.states[from_state].add_transition(symbol, to_state)
        if symbol != 'ε':
            self.alphabet.add(symbol)