import csv
from typing import List, Dict, Set, Tuple
from collections import deque
import sys
from collections import defaultdict
import traceback


class MooreTransition:
    def __init__(self, from_state: int, to_states: Set[int], in_symbol: str):
        self.from_state = from_state
        self.to_states = to_states
        self.in_symbol = in_symbol


class MooreState:
    def __init__(self, state: str, out_symbol: str, transitions=None):
        if transitions is None:
            transitions = set()
        self.state = state
        self.out_symbol = out_symbol
        self.transitions = transitions


class MooreChain:
    def __init__(self, state: str = "", state_ind: int = 0, chained_states=None):
        if chained_states is None:
            chained_states = set()
        self.state = state
        self.state_ind = state_ind
        self.chained_states = chained_states


class DetermineNFA:
    def __init__(self):
        self.m_in_symbols: List[str] = []
        self.m_states: List[MooreState] = []
        self.m_states_map: Dict[str, int] = {}
        self.m_chained_states: List[MooreChain] = []
        self.m_transitions: List[MooreTransition] = []

    def read_from_csv_file(self, file_name: str):
        try:
            with open(file_name, 'r') as file:
                csv_reader = csv.reader(file, delimiter=';')
                out_symbols = next(csv_reader)
                states = next(csv_reader)
                out_symbols = out_symbols[1:]
                states = states[1:]

                for state, out_symbol in zip(states, out_symbols):
                    if state and state != '""' and out_symbol != '""':
                        self.m_states.append(MooreState(state, out_symbol, set()))
                        self.m_states_map[state] = len(self.m_states) - 1
                    else:
                        raise ValueError("Wrong states format")
                for row in csv_reader:
                    if row:
                        in_symbol = row[0]
                        self.m_in_symbols.append(in_symbol)

                        for index, transition in enumerate(row[1:]):
                            if transition and transition != '""':
                                transition_set = set(self.m_states_map[to_state] for to_state in transition.split(','))
                                self.m_transitions.append(MooreTransition(index, transition_set, in_symbol))
                                self.m_states[index].transitions.add(len(self.m_transitions) - 1)
        except FileNotFoundError:
            raise RuntimeError(f"Could not open file: {file_name}")

    def find_chain(self):
        self.m_chained_states: List[MooreChain] = []

        for i, state in enumerate(self.m_states):
            chained_states: Dict[str, Set[int]] = {}
            transition_set: Set[int] = {i}
            chained_states[state.state] = set()

            state_queue = deque([state])
            while state_queue:
                current_state = state_queue.popleft()

                for transition_ind in current_state.transitions:
                    transition = self.m_transitions[transition_ind]
                    if transition.in_symbol in ("ε", "Оµ"):
                        to_states_set = transition.to_states
                        transition_set.update(to_states_set)
                        for to_state_ind in to_states_set:
                            to_state = self.m_states[to_state_ind]
                            if to_state.state not in chained_states:
                                state_queue.append(to_state)
                            else:
                                transition_set.update(chained_states[to_state.state])

            self.m_chained_states.append(MooreChain(state.state, i, transition_set))

    def convert_to_dfa(self):
        new_chained_state_map: Dict[str, MooreChain] = {}
        new_states: List[MooreState] = []
        new_transitions: List[MooreTransition] = []
        ch_st_start = self.m_chained_states[0]
        st_start = self.m_states[ch_st_start.state_ind]
        new_chained_state_map[ch_st_start.state] = MooreChain(ch_st_start.state, 0, ch_st_start.chained_states)
        new_states.append(MooreState(st_start.state, st_start.out_symbol, set()))
        for chained_state_ind in ch_st_start.chained_states:
            if self.m_states[chained_state_ind].out_symbol:
                new_states[0].out_symbol = self.m_states[chained_state_ind].out_symbol
                break
        state_queue = deque([new_chained_state_map[self.m_chained_states[0].state]])
        while state_queue:
            ch_state = state_queue.popleft()
            for in_symbol in self.m_in_symbols:
                to_new_state_by_in_symbol: Set[int] = set()
                for chained_state_ind in ch_state.chained_states:
                    for transition_ind in self.m_states[chained_state_ind].transitions:
                        transition = self.m_transitions[transition_ind]
                        if transition.in_symbol == in_symbol:
                            to_new_state_by_in_symbol.update(transition.to_states)
                if not to_new_state_by_in_symbol:
                    continue
                new_to_state_name = ''.join(self.m_states[state_ind].state for state_ind in to_new_state_by_in_symbol)
                if new_to_state_name in new_chained_state_map:
                    new_transitions.append(
                        MooreTransition(ch_state.state_ind, {new_chained_state_map[new_to_state_name].state_ind},
                                        in_symbol))
                    new_states[ch_state.state_ind].transitions.add(len(new_transitions) - 1)
                    continue
                to_states: Set[int] = set()
                for state_ind in to_new_state_by_in_symbol:
                    for transition_ind in self.m_states[state_ind].transitions:
                        transition = self.m_transitions[transition_ind]
                        to_states.update(transition.to_states)
                new_states[ch_state.state_ind].transitions.add(len(new_transitions))
                out_symbol = next((self.m_states[state_ind].out_symbol for state_ind in to_states if
                                   self.m_states[state_ind].out_symbol), '')
                new_states.append(MooreState(new_to_state_name, out_symbol, set()))
                new_transitions.append(MooreTransition(ch_state.state_ind, {len(new_states) - 1}, in_symbol))
                new_chained_state_map[new_to_state_name] = MooreChain(new_to_state_name, len(new_states) - 1, to_states)
                state_queue.append(new_chained_state_map[new_to_state_name])
        self.m_chained_states = list(new_chained_state_map.values())
        self.m_states = new_states
        self.m_states_map.clear()
        self.m_transitions = new_transitions

    def to_dfa(self):
        self.find_chain()
        if "ε" in self.m_in_symbols:
            self.m_in_symbols.remove("ε")
        self.convert_to_dfa()
        self.trim_in_symbols()

    def trim_in_symbols(self):
        self.m_in_symbols = [
            symbol for symbol in self.m_in_symbols
            if any(t.in_symbol == symbol for t in self.m_transitions)
        ]

    def write_to_csv_file(self, filename: str):
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([''] + [state.out_symbol for state in self.m_states])
                writer.writerow([''] + [state.state for state in self.m_states])
                for in_symbol in self.m_in_symbols:
                    row = [in_symbol]
                    for state in self.m_states:
                        transition_found = False
                        for transition_index in state.transitions:
                            transition = self.m_transitions[transition_index]
                            if transition.in_symbol == in_symbol:
                                to_state = next(iter(transition.to_states), -1)
                                row.append(self.m_states[to_state].state if to_state != -1 else '')
                                transition_found = True
                                break
                        if not transition_found:
                            row.append('')
                    writer.writerow(row)

        except IOError:
            raise ValueError(f"Can't open file {filename}")

    def unique_names(self, temp: Dict[str, Dict[str, Set[int]]]) -> int:
        return sum(len(state_map) for state_map in temp.values())

    def minimize(self):
        state_map: Dict[str, Dict[str, Set[int]]] = defaultdict(lambda: defaultdict(set))
        for i, state in enumerate(self.m_states):
            state_map[state.out_symbol][state.state].add(i)
        state_converter: Dict[str, Tuple[int, str]] = {}
        new_state = 'A'
        new_state_index = 0
        for out_combination, state_groups in state_map.items():
            for state, state_indexes in state_groups.items():
                for state_ind in state_indexes:
                    state_converter[state] = (state_ind, f"{new_state}{new_state_index}")
            new_state_index += 1
        new_state = chr(ord(new_state) + 1)
        while self.unique_names(state_map) != self.unique_names(state_map_temp := {}):
            state_converter_temp = state_converter.copy()
            state_converter.clear()
            state_map_temp = state_map.copy()
            state_map.clear()
            new_state_index = 0
            for out_combination, state_groups in state_map_temp.items():
                help_map: Dict[str, str] = {}
                for state, state_indexes in state_groups.items():
                    for state_index in state_indexes:
                        new_state_transition = ''.join(
                            state_converter_temp[
                                self.m_states[next(iter(self.m_transitions[transition_ind].to_states))].state][1]
                            for transition_ind in self.m_states[state_index].transitions
                        )
                        if new_state_transition not in help_map:
                            new_name = f"{new_state}{new_state_index}"
                            new_state_index += 1
                            help_map[new_state_transition] = new_name
                            state_converter[self.m_states[state_index].state] = (state_index, new_name)
                            state_map[out_combination][new_name].add(state_index)
                        else:
                            state_converter[self.m_states[state_index].state] = (
                                state_index, help_map[new_state_transition])
                            state_map[out_combination][help_map[new_state_transition]].add(state_index)
            new_state = chr(ord(new_state) + 1)
        to_new_states_map: Dict[int, str] = {}
        for out_combination, state_groups in state_map.items():
            for group_name, states_set in state_groups.items():
                for state_index in states_set:
                    to_new_states_map[state_index] = group_name
        new_states: List[MooreState] = [
            MooreState(to_new_states_map[0], self.m_states[0].out_symbol, self.m_states[0].transitions)]
        new_transitions: List[MooreTransition] = []
        replaced_names: Set[str] = set()
        for out_symbol_comb, new_names_map in state_map.items():
            for group_name, states_set in new_names_map.items():
                if 0 in states_set or group_name in replaced_names:
                    continue
                new_states.append(MooreState(group_name, self.m_states[next(iter(states_set))].out_symbol,
                                             self.m_states[next(iter(states_set))].transitions))
                replaced_names.add(group_name)
        for from_index, (group_name, out_symbol, transitions_set) in enumerate(new_states):
            new_transitions_set = set()
            for transition_ind in transitions_set:
                transition = self.m_transitions[transition_ind]
                to_state_string = to_new_states_map[next(iter(transition.to_states))]
                to_index = next(i for i, state in enumerate(new_states) if state.state == to_state_string)
                new_transitions.append(MooreTransition(from_index, {to_index}, transition.in_symbol))
                new_transitions_set.add(len(new_transitions) - 1)
            new_states[from_index].transitions = new_transitions_set
        for old_index, new_name in to_new_states_map.items():
            print(f"{self.m_states[old_index].state}->{new_name}")

        self.m_states = new_states
        self.m_transitions = new_transitions


def main():
    if len(sys.argv) not in [3, 4]:
        print("Usage: python script.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) == 4:
        input_file = sys.argv[2]
        output_file = sys.argv[3]
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    try:
        dnfa = DetermineNFA()
        dnfa.read_from_csv_file(input_file)
        dnfa.to_dfa()
        dnfa.write_to_csv_file(output_file)
    except Exception as e:
        print(traceback.format_exc())
        print(str(e))


if __name__ == "__main__":
    main()
