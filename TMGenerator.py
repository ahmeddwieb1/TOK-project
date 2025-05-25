from Automaton import Automaton

class TMGenerator:
    @staticmethod
    def generate_transitions(dfa: Automaton) -> list:
        """
        Generate Turing Machine transitions from DFA
        Returns list of transitions in the format:
        {
            'current_state': str,
            'read_symbol': str,
            'write_symbol': str,
            'move': str ('L', 'R', or 'H'),
            'next_state': str
        }
        """
        transitions = []
        alphabet = sorted(dfa.alphabet)
        blank_symbol = '#'  # Using # instead of B for blank

        # Add transitions for each state and symbol
        for state_name, state in dfa.states.items():
            for symbol in alphabet:
                if symbol in state.transitions:
                    next_state = next(iter(state.transitions[symbol]))
                    transitions.append({
                        'current_state': state_name,
                        'read_symbol': symbol,
                        'write_symbol': symbol,  # Keep same symbol by default
                        'move': 'R',  # Always move right
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

    @staticmethod
    def simulate_tm(transitions: list, input_str: str) -> dict:
        """
        Simulate the Turing Machine on given input
        Returns dictionary with result and tape snapshot
        """
        tape = list(input_str)
        head_pos = 0
        current_state = 'q0'  # Assuming q0 is the initial state
        blank_symbol = '#'
        max_steps = 1000  # Prevent infinite loops
        step_count = 0

        while step_count < max_steps:
            # Read current symbol (use blank if beyond tape)
            current_symbol = tape[head_pos] if head_pos < len(tape) else blank_symbol

            # Find matching transition
            transition = next((t for t in transitions
                            if t['current_state'] == current_state
                            and t['read_symbol'] == current_symbol), None)

            if not transition:
                return {
                    'result': 'reject',
                    'tape': ''.join(tape),
                    'reason': 'No transition found',
                    'head_pos': head_pos
                }

            # Write symbol to tape
            if head_pos < len(tape):
                tape[head_pos] = transition['write_symbol']
            else:
                tape.append(transition['write_symbol'])

            # Check for halting states
            if transition['next_state'] == 'accept':
                return {
                    'result': 'accept',
                    'tape': ''.join(tape),
                    'head_pos': head_pos
                }
            elif transition['next_state'] == 'reject':
                return {
                    'result': 'reject',
                    'tape': ''.join(tape),
                    'head_pos': head_pos
                }

            # Move head
            if transition['move'] == 'R':
                head_pos += 1
            elif transition['move'] == 'L':
                head_pos -= 1
                if head_pos < 0:
                    head_pos = 0  # Stay at left end

            current_state = transition['next_state']
            step_count += 1

        return {
            'result': 'reject',
            'tape': ''.join(tape),
            'reason': 'Maximum steps exceeded',
            'head_pos': head_pos
        }