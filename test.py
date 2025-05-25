import re
from collections import defaultdict, deque
from typing import Set, Dict, List, Tuple


class State:
    def __init__(self, name: str):
        self.name = name
        self.is_final = False
        self.transitions = defaultdict(set)


class NFA:
    def __init__(self):
        self.states = {}
        self.start_state = None
        self.final_states = set()
        self.alphabet = set()

    def add_state(self, name: str) -> State:
        if name not in self.states:
            self.states[name] = State(name)
        return self.states[name]

    def add_transition(self, from_state: str, to_state: str, symbol: str):
        self.states[from_state].transitions[symbol].add(to_state)
        if symbol != 'ε':
            self.alphabet.add(symbol)


class DFA:
    def __init__(self):
        self.states = {}
        self.start_state = None
        self.final_states = set()
        self.alphabet = set()

    def add_state(self, name: str) -> State:
        if name not in self.states:
            self.states[name] = State(name)
        return self.states[name]

    def add_transition(self, from_state: str, to_state: str, symbol: str):
        self.states[from_state].transitions[symbol].add(to_state)
        self.alphabet.add(symbol)


def insert_concat(regex: str) -> str:
    """Insert explicit concatenation operator '.' where needed."""
    result = ''
    for i in range(len(regex)):
        c1 = regex[i]
        result += c1
        if i + 1 < len(regex):
            c2 = regex[i + 1]
            if (c1.isalnum() or c1 in ')*}') and (c2.isalnum() or c2 in '({['):
                result += '.'
    return result


def to_postfix(regex: str) -> str:
    """Convert infix regex to postfix using the Shunting Yard algorithm."""
    precedence = {'*': 3, '.': 2, '|': 1}
    output = []
    stack = []
    for c in regex:
        if c.isalnum() or c in {'+', '-', '/', '[', ']', '{', '}'}:
            output.append(c)
        elif c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Remove '('
        elif c in precedence:
            while (stack and stack[-1] != '(' and
                   precedence.get(stack[-1], 0) >= precedence[c]):
                output.append(stack.pop())
            stack.append(c)
    while stack:
        output.append(stack.pop())
    return ''.join(output)


def regex_to_nfa(regex: str) -> NFA:
    nfa = NFA()
    if not regex:
        # Handle empty string case
        start = "q0"
        nfa.add_state(start)
        nfa.start_state = start
        nfa.final_states.add(start)
        nfa.states[start].is_final = True
        return nfa

    # Step 1: Insert explicit concatenation
    regex = insert_concat(regex)
    # Step 2: Convert to postfix
    postfix = to_postfix(regex)

    stack = []
    state_counter = 0

    def new_state():
        nonlocal state_counter
        state_counter += 1
        return f"q{state_counter}"

    def basic_nfa(symbol: str) -> Tuple[str, str]:
        start = new_state()
        end = new_state()
        nfa.add_state(start)
        nfa.add_state(end)
        nfa.add_transition(start, end, symbol)
        return start, end

    def concat_nfa(nfa1: Tuple[str, str], nfa2: Tuple[str, str]) -> Tuple[str, str]:
        nfa.add_transition(nfa1[1], nfa2[0], 'ε')
        return nfa1[0], nfa2[1]

    def union_nfa(nfa1: Tuple[str, str], nfa2: Tuple[str, str]) -> Tuple[str, str]:
        start = new_state()
        end = new_state()
        nfa.add_state(start)
        nfa.add_state(end)
        nfa.add_transition(start, nfa1[0], 'ε')
        nfa.add_transition(start, nfa2[0], 'ε')
        nfa.add_transition(nfa1[1], end, 'ε')
        nfa.add_transition(nfa2[1], end, 'ε')
        return start, end

    def star_nfa(nfa1: Tuple[str, str]) -> Tuple[str, str]:
        start = new_state()
        end = new_state()
        nfa.add_state(start)
        nfa.add_state(end)
        nfa.add_transition(start, nfa1[0], 'ε')
        nfa.add_transition(nfa1[1], end, 'ε')
        nfa.add_transition(start, end, 'ε')
        nfa.add_transition(nfa1[1], nfa1[0], 'ε')
        return start, end

    for char in postfix:
        if char.isalnum() or char in {'+', '-', '/', '[', ']', '{', '}'}:
            stack.append(basic_nfa(char))
        elif char == '*':
            nfa1 = stack.pop()
            stack.append(star_nfa(nfa1))
        elif char == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(concat_nfa(nfa1, nfa2))
        elif char == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(union_nfa(nfa1, nfa2))

    if not stack:
        raise ValueError("Invalid regex: Empty expression")

    start, end = stack[0]
    nfa.start_state = start
    nfa.final_states.add(end)
    nfa.states[end].is_final = True

    return nfa


def epsilon_closure(nfa: NFA, states: Set[str]) -> Set[str]:
    closure = set(states)
    stack = list(states)

    while stack:
        state = stack.pop()
        for next_state in nfa.states[state].transitions['ε']:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)

    return closure


def nfa_to_dfa(nfa: NFA) -> DFA:
    dfa = DFA()
    initial_states = epsilon_closure(nfa, {nfa.start_state})
    state_queue = deque([(frozenset(initial_states), f"q0")])
    state_map = {frozenset(initial_states): "q0"}
    dfa.start_state = "q0"
    dfa.add_state("q0")

    while state_queue:
        nfa_states, dfa_state = state_queue.popleft()

        # Check if this DFA state should be final
        if any(state in nfa.final_states for state in nfa_states):
            dfa.final_states.add(dfa_state)
            dfa.states[dfa_state].is_final = True

        # For each symbol in the alphabet
        for symbol in nfa.alphabet:
            # Find all states reachable with this symbol
            next_states = set()
            for state in nfa_states:
                next_states.update(nfa.states[state].transitions[symbol])

            # Add epsilon closure
            next_states = epsilon_closure(nfa, next_states)

            if not next_states:
                continue

            # Create new DFA state if needed
            if frozenset(next_states) not in state_map:
                new_state_name = f"q{len(state_map)}"
                state_map[frozenset(next_states)] = new_state_name
                dfa.add_state(new_state_name)
                state_queue.append((frozenset(next_states), new_state_name))

            # Add transition
            dfa.add_transition(dfa_state, state_map[frozenset(next_states)], symbol)

    return dfa


def generate_tm_transitions(dfa: DFA) -> List[Dict]:
    transitions = []
    alphabet = sorted(list(dfa.alphabet))

    # Add transitions for each state and symbol
    for state_name, state in dfa.states.items():
        for symbol in alphabet:
            if symbol in state.transitions:
                next_state = list(state.transitions[symbol])[0]
                transitions.append({
                    'current_state': state_name,
                    'read_symbol': symbol,
                    'write_symbol': symbol,
                    'move': 'R',
                    'next_state': next_state
                })

    # Add transitions for final states
    for state_name in dfa.final_states:
        transitions.append({
            'current_state': state_name,
            'read_symbol': 'B',  # Blank symbol
            'write_symbol': 'B',
            'move': 'H',  # Halt
            'next_state': 'HALT'
        })

    return transitions


def main():
    print("Regular Expression to DFA and Turing Machine Converter")
    print("Enter a regular expression (use . for concatenation, | for union, * for Kleene star):")
    regex = input().strip()

    # Convert regex to NFA
    nfa = regex_to_nfa(regex)

    # Convert NFA to DFA
    dfa = nfa_to_dfa(nfa)

    # Generate TM transitions
    tm_transitions = generate_tm_transitions(dfa)

    # Print results
    print("\nDFA States:")
    for state_name, state in dfa.states.items():
        print(f"State: {state_name} (Final: {state.is_final})")
        for symbol, next_states in state.transitions.items():
            print(f"  {symbol} -> {list(next_states)[0]}")

    print("\nTuring Machine Transitions:")
    for transition in tm_transitions:
        print(f"({transition['current_state']}, {transition['read_symbol']}) -> "
              f"({transition['next_state']}, {transition['write_symbol']}, {transition['move']})")


if __name__ == "__main__":
    main()