import argparse
import rtn
import ntd
import m
from pyvis.network import Network


def drawGraph(states, inputToTransitions, is_mealy=True):
    net = Network(notebook=True, directed=True)

    for state in states:
        if state:
            net.add_node(state, label=state)

    for input_value, transitions in inputToTransitions.items():
        for from_state, to_state_output in transitions.items():
            if not from_state or not to_state_output:  # Пропускаем пустые значения
                continue

            to_state, output = to_state_output.split('/')

            if not to_state:
                continue

            if is_mealy:
                label = f"{input_value}/{output}"
            else:
                label = input_value

            if from_state in states and to_state in states:
                net.add_edge(from_state, to_state, label=label)
            else:
                print(f"Warning: Attempted to add edge between non-existent nodes: {from_state} -> {to_state}")

    net.show("graph.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some CSV files.')
    parser.add_argument('regex', type=str, help='Regex')

    args = parser.parse_args()
    regexToNFA = rtn.RegexToNFAConverter(args.regex)
    regexToNFA.writeResultToCsvFile('1.csv')
    ntd.determine_nfa('1.csv', '2.csv')

    values = m.read_moore_machine('2.csv')
    values = m.removeUnreachableStates(*values)
    values = m.removeUnreachableStates(*values)
    m.writeMoore('3.csv', *values)
    moore_states, inputToTransitions = m.readMooreFromCSV('3.csv')
    drawGraph(moore_states, inputToTransitions, is_mealy=False)
