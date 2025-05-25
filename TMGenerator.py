from Automaton import Automaton

class TMGenerator:
    @staticmethod
    def generate_transitions(dfa: Automaton) -> list:

        transitions = []
        alphabet = sorted(dfa.alphabet)
        blank_symbol = 'ε'

        # Add transitions for each state and symbol
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
                    # No transition for this symbol - go to reject state
                    transitions.append({
                        'current_state': state_name,
                        'read_symbol': symbol,
                        'write_symbol': 'N',  # Mark rejection
                        'move': 'H',  # Halt immediately
                        'next_state': 'reject'
                    })

            # Handle blank symbol transitions for final states
            if state.is_final:
                transitions.append({
                    'current_state': state_name,
                    'read_symbol': blank_symbol,
                    'write_symbol': 'Y',  # Mark acceptance
                    'move': 'H',  # Halt immediately
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

