from Automaton import Automaton
from RegexParser import RegexParser


class NFAConstructor:
    def __init__(self):
        self.state_counter = 0

    def new_state(self) -> str:
        self.state_counter += 1
        return f"q{self.state_counter}"

    def build_nfa(self, regex: str) -> Automaton:
        nfa = Automaton()
        if not regex:
            start = self.new_state()
            nfa.add_state(start)
            nfa.start_state = start
            nfa.final_states.add(start)
            nfa.states[start].is_final = True
            return nfa

        postfix = RegexParser.to_postfix(RegexParser.insert(regex))
        stack = []

        for char in postfix:
            if char.isalnum() or char in {'+', '-', '/', '[', ']', '{', '}'}:
                stack.append(self._basic_nfa(nfa, char))
            elif char == '*':
                stack.append(self._star_nfa(nfa, stack.pop()))
            elif char == '.':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(self._concat_nfa(nfa, nfa1, nfa2))
            elif char == '|':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(self._union_nfa(nfa, nfa1, nfa2))

        if not stack:
            raise ValueError("Invalid regex")

        start, end = stack[0]
        nfa.start_state = start
        nfa.final_states.add(end)
        nfa.states[end].is_final = True

        return nfa

    def _basic_nfa(self, nfa: Automaton, symbol: str) -> tuple:
        start = self.new_state()
        end = self.new_state()
        nfa.add_state(start)
        nfa.add_state(end)
        nfa.add_transition(start, end, symbol)
        return (start, end)

    def _concat_nfa(self, nfa: Automaton, nfa1: tuple, nfa2: tuple) -> tuple:
        nfa.add_transition(nfa1[1], nfa2[0], 'ε')
        return (nfa1[0], nfa2[1])

    def _union_nfa(self, nfa: Automaton, nfa1: tuple, nfa2: tuple) -> tuple:
        start = self.new_state()
        end = self.new_state()
        nfa.add_state(start)
        nfa.add_state(end)
        nfa.add_transition(start, nfa1[0], 'ε')
        nfa.add_transition(start, nfa2[0], 'ε')
        nfa.add_transition(nfa1[1], end, 'ε')
        nfa.add_transition(nfa2[1], end, 'ε')
        return (start, end)

    def _star_nfa(self, nfa: Automaton, nfa1: tuple) -> tuple:
        start = self.new_state()
        end = self.new_state()
        nfa.add_state(start)
        nfa.add_state(end)
        nfa.add_transition(start, nfa1[0], 'ε')
        nfa.add_transition(nfa1[1], end, 'ε')
        nfa.add_transition(start, end, 'ε')
        nfa.add_transition(nfa1[1], nfa1[0], 'ε')
        return (start, end)