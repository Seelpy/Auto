class RegexNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class State:
    def __init__(self):
        self.transitions = {}
        self.epsilon_transitions = []

    def add_transition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)

    def add_epsilon_transition(self, state):
        self.epsilon_transitions.append(state)


class NFA:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state


def is_literal(value):
    return value not in "+*()|"


def parse_regex(expression):
    def parse(tokens):
        def get_next():
            return tokens.pop(0) if tokens else None

        def parse_primary():
            token = get_next()
            if token == "\\":
                escaped = get_next()
                if is_literal(escaped):
                    tokens.insert(0, escaped)
                else:
                    return RegexNode(escaped)
            if is_literal(token):
                return RegexNode(token)
            elif token == "(":
                node = parse_expression()
                if get_next() != ")":
                    raise ValueError("Mismatched parentheses")
                return node
            raise ValueError(f"Unexpected token: {token}")

        def parse_factor():
            node = parse_primary()
            while tokens and tokens[0] in ("*", "+"):
                op = "multiply" if get_next() == "*" else "add"
                node = RegexNode(op, left=node)
            return node

        def parse_term():
            node = parse_factor()
            while tokens and tokens[0] and (is_literal(tokens[0]) or tokens[0] == "("):
                right = parse_factor()
                node = RegexNode("concat", left=node, right=right)
            return node

        def parse_expression():
            node = parse_term()
            while tokens and tokens[0] == "|":
                get_next()
                right = parse_term()
                node = RegexNode("or", left=node, right=right)
            return node

        return parse_expression()

    tokens = list(expression)
    return parse(tokens)


def build_nfa(node):
    if node is None:
        return None

    if node.value not in ("concat", "or", "add", "multiply"):
        start = State()
        accept = State()
        start.add_transition(node.value, accept)
        return NFA(start, accept)
    elif node.value == "concat":
        left_nfa = build_nfa(node.left)
        right_nfa = build_nfa(node.right)
        left_nfa.accept_state.add_epsilon_transition(right_nfa.start_state)
        return NFA(left_nfa.start_state, right_nfa.accept_state)
    elif node.value == "or":
        start = State()
        accept = State()
        left_nfa = build_nfa(node.left)
        right_nfa = build_nfa(node.right)
        start.add_epsilon_transition(left_nfa.start_state)
        start.add_epsilon_transition(right_nfa.start_state)
        left_nfa.accept_state.add_epsilon_transition(accept)
        right_nfa.accept_state.add_epsilon_transition(accept)
        return NFA(start, accept)
    elif node.value == "multiply":
        start = State()
        accept = State()
        sub_nfa = build_nfa(node.left)
        start.add_epsilon_transition(sub_nfa.start_state)
        start.add_epsilon_transition(accept)
        sub_nfa.accept_state.add_epsilon_transition(sub_nfa.start_state)
        sub_nfa.accept_state.add_epsilon_transition(accept)
        return NFA(start, accept)
    elif node.value == "add":
        start = State()
        accept = State()
        sub_nfa = build_nfa(node.left)
        start.add_epsilon_transition(sub_nfa.start_state)
        sub_nfa.accept_state.add_epsilon_transition(sub_nfa.start_state)
        sub_nfa.accept_state.add_epsilon_transition(accept)
        return NFA(start, accept)

    raise ValueError(f"Unexpected node value: {node.value}")


def adapt_nfa(nfa: NFA):
    state_index = {}
    index = 0

    def assign_indices(state):
        nonlocal index
        if state not in state_index:
            state_index[state] = f"S{index}"
            index += 1
            for symbol, states in state.transitions.items():
                for s in states:
                    assign_indices(s)
            for s in state.epsilon_transitions:
                assign_indices(s)

    assign_indices(nfa.start_state)

    initial_state = state_index[nfa.start_state]
    finite_state = state_index[nfa.accept_state]

    machine = {state_index[s]: {"is_finite": name == finite_state, "transitions": {}} for s, name in
               state_index.items()}

    for state, name in state_index.items():
        for symbol, states in state.transitions.items():
            machine[name]["transitions"].setdefault(symbol, set()).update(state_index[s] for s in states)
        for s in state.epsilon_transitions:
            machine[name]["transitions"].setdefault("ε", set()).add(state_index[s])

    symbols = set()
    for state in machine:
        trans = machine[state]["transitions"]
        for symbol in trans:
            symbols.add(symbol)

    for state in machine:
        for symbol in symbols:
            machine[state]["transitions"].setdefault(symbol, set())

    return initial_state, finite_state, machine


def process_regex(regex_pattern):
    tree = parse_regex(regex_pattern)
    nfa = build_nfa(tree)
    return adapt_nfa(nfa)