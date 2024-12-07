import csv
from collections import defaultdict, deque
import sys
import traceback


class Determiner:
    def __init__(self):
        self.nfa = self.NFA()
        self.dfa = self.DFA()

    class NFA:
        def __init__(self):
            self.states = []
            self.alphabet = []
            self.transitions = defaultdict(lambda: defaultdict(list))
            self.start_state = None
            self.final_states = []

    class DFA:
        def __init__(self):
            self.states = set()
            self.alphabet = []
            self.transitions = {}
            self.final_states = set()
            self.start_state = None

    def read_nfa(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            headers = next(reader)

            # Read states and final states
            states_line = next(reader)
            for i, cell in enumerate(states_line):
                if cell:
                    self.nfa.states.append(cell)
                    if headers[i] == "F":
                        self.nfa.final_states.append(cell)

            # Read alphabet and transitions
            for row in reader:
                if row[0]:
                    symbol = row[0]
                    self.nfa.alphabet.append(symbol)
                    for i, cell in enumerate(row[1:], start=0):
                        if cell:
                            destinations = cell.split(',')
                            for destination in destinations:
                                self.nfa.transitions[self.nfa.states[i]][symbol].append(destination)

        if self.nfa.states:
            self.nfa.start_state = self.nfa.states[0]

    def convert_to_dfa(self):
        self.build_dfa_transition_table()

    def write_dfa_to_file(self, filename):
        with open(filename, 'w') as file:
            renamed_state = {state: f"q{i}" for i, state in enumerate(self.dfa.transitions.keys())}

            # Write final states
            file.write(";")
            if self.dfa.start_state in self.dfa.final_states:
                file.write("F")
            for state in self.dfa.transitions.keys():
                if state != self.dfa.start_state:
                    file.write(f";{'F' if state in self.dfa.final_states else ''}")

            file.write("\n")

            # Write states
            file.write(";")
            file.write(renamed_state[self.dfa.start_state])
            for state in self.dfa.transitions.keys():
                if state != self.dfa.start_state:
                    file.write(f";{renamed_state[state]}")
            file.write("\n")

            # Write transitions
            for symbol in self.dfa.alphabet:
                line = [symbol]
                for state in self.dfa.transitions.keys():
                    next_state = self.dfa.transitions[state].get(symbol, "-")
                    line.append(renamed_state[next_state] if next_state != "-" else "-")
                file.write(";".join(line) + "\n")

    def epsilon_closure(self, state):
        closure = {state}
        to_process = deque([state])

        while to_process:
            current = to_process.popleft()
            if current in self.nfa.transitions and "ε" in self.nfa.transitions[current]:
                for next_state in self.nfa.transitions[current]["ε"]:
                    if next_state not in closure:
                        closure.add(next_state)
                        to_process.append(next_state)

        return closure

    def build_dfa_transition_table(self):
        state_queue = deque()

        start_closure = self.epsilon_closure(self.nfa.start_state)
        state_queue.append(start_closure)

        processed_states = {frozenset(start_closure): "X0"}
        self.dfa.start_state = "X0"

        dfa_alphabet = [symbol for symbol in self.nfa.alphabet if symbol != 'ε']
        self.dfa.alphabet = dfa_alphabet

        if any(state in self.nfa.final_states for state in start_closure):
            self.dfa.final_states.add("X0")

        state_counter = 1

        while state_queue:
            current_states = state_queue.popleft()
            current_state_name = processed_states[frozenset(current_states)]

            for symbol in dfa_alphabet:
                reachable = set()

                for state in current_states:
                    if state in self.nfa.transitions and symbol in self.nfa.transitions[state]:
                        for next_state in self.nfa.transitions[state][symbol]:
                            closure = self.epsilon_closure(next_state)
                            reachable.update(closure)

                if reachable:
                    frozen_reachable = frozenset(reachable)
                    if frozen_reachable not in processed_states:
                        new_state_name = f"X{state_counter}"
                        processed_states[frozen_reachable] = new_state_name
                        state_queue.append(reachable)

                        if any(state in self.nfa.final_states for state in reachable):
                            self.dfa.final_states.add(new_state_name)

                        state_counter += 1

                    self.dfa.transitions.setdefault(current_state_name, {})[symbol] = processed_states[frozen_reachable]
                else:
                    self.dfa.transitions.setdefault(current_state_name, {})[symbol] = "-"


def determine_nfa(input_file, output_file):
    try:
        determiner = Determiner()
        determiner.read_nfa(input_file)
        determiner.convert_to_dfa()
        determiner.write_dfa_to_file(output_file)
    except Exception as ex:
        print(f"Error: {ex}", file=sys.stderr)
        traceback.print_exc()


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} in.csv out.csv", file=sys.stderr)
        return 1

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    try:
        determine_nfa(input_file, output_file)
    except Exception as ex:
        print(ex)
        traceback.print_exc()


if __name__ == "__main__":
    main()
