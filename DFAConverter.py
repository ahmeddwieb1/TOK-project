from collections import deque
from Automaton import Automaton


class DFAConverter:
    @staticmethod
    def epsilon_closure(nfa: Automaton, states: set) -> set:
        closure = set(states)
        queue = deque(states)

        while queue:
            state = queue.popleft()
            #  Check if state exists
            if state in nfa.states:
                for next_state in nfa.states[state].transitions.get('ε', set()):
                    if next_state not in closure:
                        closure.add(next_state)
                        queue.append(next_state)

        return closure

    @staticmethod
    def nfa_to_dfa(nfa: Automaton) -> Automaton:
        dfa = Automaton()

        initial_closure = DFAConverter.epsilon_closure(nfa, {nfa.start_state})
        state_queue = deque([(frozenset(initial_closure), "q0")])
        state_map = {frozenset(initial_closure): "q0"}
        dfa.start_state = "q0"
        dfa.add_state("q0")

        dead_state = "DEAD"
        dfa.add_state(dead_state)

        while state_queue:
            nfa_states, dfa_state = state_queue.popleft()
            # Check if this is a final state
            if any(state in nfa.final_states for state in nfa_states):
                dfa.final_states.add(dfa_state)
                dfa.states[dfa_state].is_final = True

            for symbol in nfa.alphabet:
                next_states = set()
                for state in nfa_states:
                    next_states.update(nfa.states[state].transitions.get(symbol, set()))
                # No transition for this symbol
                if not next_states:
                    dfa.add_transition(dfa_state, dead_state, symbol)
                    continue

                next_closure = DFAConverter.epsilon_closure(nfa, next_states)

                if not next_closure:
                    dfa.add_transition(dfa_state, dead_state, symbol)
                    continue

                if frozenset(next_closure) not in state_map:
                    new_state_name = f"q{len(state_map)}"
                    state_map[frozenset(next_closure)] = new_state_name
                    dfa.add_state(new_state_name)
                    state_queue.append((frozenset(next_closure), new_state_name))

                dfa.add_transition(dfa_state, state_map[frozenset(next_closure)], symbol)

        for symbol in nfa.alphabet:
            dfa.add_transition(dead_state, dead_state, symbol)

        return dfa