from Automaton import Automaton

class TMGenerator:
    @staticmethod
    def generate_transitions(dfa: Automaton) -> list:

        transitions = []
        alphabet = sorted(dfa.alphabet)
        blank_symbol = 'ε'


        for state_name, state in dfa.states.items():
            for symbol in alphabet:
                if symbol in state.transitions:
                    next_state = next(iter(state.transitions[symbol]))
                    transitions.append({
                        'current_state': state_name,
                        'read_symbol': symbol,
                        'write_symbol': symbol,
                        'move': 'R',
                        'next_state': next_state
                    })
                else:
                    transitions.append({
                        'current_state': state_name,
                        'read_symbol': symbol,
                        'write_symbol': 'N',
                        'move': 'H',
                        'next_state': 'reject'
                    })

            if state.is_final:
                transitions.append({
                    'current_state': state_name,
                    'read_symbol': blank_symbol,
                    'write_symbol': 'Y',
                    'move': 'H',
                    'next_state': 'accept'
                })
            else:
                transitions.append({
                    'current_state': state_name,
                    'read_symbol': blank_symbol,
                    'write_symbol': 'N',  # Mark rejection
                    'move': 'H',  # Halt immediately
                    'next_state': 'reject'
                })

        return transitions

