from DFAConverter import DFAConverter
from NFAConstructor import NFAConstructor
from TMGenerator import TMGenerator


class Main:
    @staticmethod
    def run():
        print("=== Regular Expression to DFA and Turing Machine Converter ===")
        print("Operators: . (concat), | (union), * (Kleene star), + (Kleene plus), ")

        while True:
            regex = input("Enter regular expression: ").strip()

            if regex.lower() == 'exit':
                print("Exiting program...")
                break

            if not regex:
                print("Error: Empty input. Please try again.\n")
                continue

            try:
                # Build and convert automata
                nfa = NFAConstructor().build_nfa(regex)
                dfa = DFAConverter.nfa_to_dfa(nfa)
                tm_transitions = TMGenerator.generate_transitions(dfa)

                # Display DFA information
                Main._display_dfa(dfa)

                # Display TM information
                Main._display_tm(tm_transitions)

            except Exception as e:
                print(f"Error processing regular expression: {e}\n")

    @staticmethod
    def _display_dfa(dfa):
        print("\n=== DFA Information ===")
        print(f"Alphabet: {sorted(dfa.alphabet)}")
        print(f"Start State: {dfa.start_state}")
        print("accept States:", ", ".join(dfa.final_states))

        print("\nState Transitions:")
        for state_name, state in sorted(dfa.states.items()):
            transitions = []
            for symbol, next_states in sorted(state.transitions.items()):
                next_state = next(iter(next_states))
                transitions.append(f"{symbol}→{next_state}")
            print(f"{state_name} ({'Accept State' if state.is_final else ' '}): {', '.join(transitions)}")

    @staticmethod
    def _display_tm(transitions):
        print("\n=== Turing Machine Transitions ===")

        transitions_by_state = {}
        for t in transitions:
            if t['current_state'] not in transitions_by_state:
                transitions_by_state[t['current_state']] = []
            transitions_by_state[t['current_state']].append(t)

        for state, state_transitions in sorted(transitions_by_state.items()):
            print(f"\nFrom State {state}:")
            for t in sorted(state_transitions, key=lambda x: x['read_symbol']):
                print(f"  ({t['current_state']}, {t['read_symbol']}) → "
                      f"({t['next_state']}, {t['write_symbol']}, {t['move']})")



if __name__ == "__main__":
    Main.run()