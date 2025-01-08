def fill_epsilon(machine):
    epsilon = {}

    for state in machine:
        transitions = []
        if "ε" in machine[state]["transitions"]:
            transitions = machine[state]["transitions"]["ε"]
        visited = set()
        stack = [state]

        while stack:
            vertex = stack.pop()

            if vertex not in visited:
                visited.add(vertex)

                if "ε" not in machine[vertex]["transitions"]:
                    continue
                for neighbor in machine[vertex]["transitions"]["ε"]:
                    if neighbor:
                        stack.append(neighbor)

        epsilon[state] = list(visited)

    return epsilon


def get_dependencies(states, epsilon):
    dependencies = set()

    for state in states:
        dependencies.add(state)
        for transition in epsilon[state]:
            dependencies.add(transition)

    return list(dependencies)


def find_key_with_value(dictionary, new_value):
    for key, value in dictionary.items():
        if tuple(sorted(value)) == tuple(sorted(new_value)):
            return key

    return None


def create_dfa(initial_state, finite_state, epsilon, machine):
    s_count = 0
    state_dependencies = {"s0": [initial_state]}
    states = ["s0"]
    new_machine = {}

    for state in states:
        new_machine[state] = {
            "is_finite": finite_state in get_dependencies(state_dependencies[state], epsilon),
            "transitions": {}
        }

        for symbol in filter(lambda x: x != "ε", machine[initial_state]["transitions"]):
            transitions = []
            for dependency in get_dependencies(state_dependencies[state], epsilon):
                transitions.extend(machine[dependency]["transitions"][symbol])
            transitions = list(set(transitions))
            key = ''
            if len(transitions) != 0:
                key = find_key_with_value(state_dependencies, transitions)
            if key is None:
                s_count += 1
                key = f"s{s_count}"
                states.append(key)
                state_dependencies[key] = transitions
            new_machine[state]["transitions"][symbol] = key

    return new_machine


def adapt_dfa(initial_state, machine):
    states = machine.keys()
    input_symbols = machine[initial_state]["transitions"].keys()
    outputs = {}
    transitions = {}
    for state in states:
        outputs[state] = "F" if machine[state]["is_finite"] else ""
        transitions[state] = {}
        for symbol in input_symbols:
            transitions[state][symbol] = machine[state]["transitions"][symbol]

    return states, input_symbols, transitions, outputs, initial_state


def process_nfa(initial_state, finite_state, machine):
    epsilon = fill_epsilon(machine)
    dfa = create_dfa(initial_state, finite_state, epsilon, machine)
    return adapt_dfa("s0", dfa)