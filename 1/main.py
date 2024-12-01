from __future__ import annotations
import re
import csv
import argparse


class Transition:
    def __init__(self, x1: str, y: str, x2: str | None):
        self.x1 = x1
        self.x2 = x2
        self.y = y

class Gramma:
    def __init__(self, isLeft: bool, transitions: list[Transition]):
        self.transitions = transitions
        self.isLeft = isLeft
    def alphabet(self) -> list[str]:
        a = set()
        for transition in self.transitions:
            a.add(transition.y)
        return list(a)

class State:
    def __init__(self, state: str, isEnd: bool, isStart: bool):
        self.state = state
        self.isEnd = isEnd
        self.isStart = isStart

class MooreMachine:
    def __init__(self, states: list[State], inputs: list[str], transitions: dict):
        self.states = states
        self.inputs = inputs
        self.transitions = transitions

class StateAlias:
    def __init__(self):
        self.alias: dict = {}
        self.index = 0
    def add(self, state: str, isEnd: bool = False, isStart: bool = False) -> str:
        if state in self.alias:
            return self.alias[state].state
        s = 'q' + str(self.index)
        self.alias[state] = State(s, isEnd, isStart)
        self.index += 1
        return s
    def get(self, state: str):
        return self.alias[state].state
    def list(self) -> list[State]:
        return list(self.alias.values())
    def print(self):
        for k in self.alias.keys():
            print(k, self.alias[k].state)

def ConvertGrammarToMoore(gramma: Gramma) -> MooreMachine:
    transitions = {}
    inputs = gramma.alphabet()
    aliases = StateAlias()

    if gramma.isLeft:
        aliases.add('H', False, True)
        aliases.add(gramma.transitions[0].x1, True)
    else:
        aliases.add('F', True)
        aliases.add(gramma.transitions[0].x1, False, True)

    # Создаем состояния для каждого нетерминала
    for transition in gramma.transitions:
        if transition.x1 is not None:
            aliases.add(transition.x1)
        if transition.x2 is not None:
            aliases.add(transition.x2)

    # Определяем переходы в зависимости от типа грамматики
    for transition in gramma.transitions:
        to = None
        frm = None
        if not gramma.isLeft:
            frm = (aliases.get(transition.x1), transition.y)
            if transition.x2 is None:
                to = aliases.get('F')
            else:
                to = aliases.get(transition.x2)
        else:
            to = aliases.get(transition.x1)
            if transition.x2 is None:
                frm = (aliases.get("H"), transition.y)
            else:
                frm = (aliases.get(transition.x2), transition.y)
        if frm not in transitions:
            transitions[frm] = []
        transitions[frm].append(to)

    aliases.print()

    return MooreMachine(aliases.list(), inputs, transitions)

def ReadGramma(data: str) -> Gramma:
    print(data)

    isLeftPatter = re.compile(r'<\w+>\s*[\wε]', re.MULTILINE)
    isLeft = bool(len(isLeftPatter.findall(data)) > 0)

    pattern = r'^\s*<(\w+)>\s*->\s*([\wε](?:\s+<\w+>)?(?:\s*\|\s*[\wε](?:\s+<\w+>)?)*)\s*$'
    if isLeft:
        pattern = r'^\s*<(\w+)>\s*->\s*((?:<\w+>\s+)?[\wε](?:\s*\|\s*(?:<\w+>\s+)?[\wε])*)\s*$'

    p = re.compile(pattern, re.MULTILINE)

    gr = Gramma(isLeft, [])
    for transit in p.findall(data):
        x1 = transit[0]
        for t in str.split(transit[1], '|'):
            tdata = str.strip(t).split(" ")
            trans = Transition("", "", None)
            trans.x1 = x1
            yi = 0
            xi = 1
            if isLeft:
                yi, xi, = xi, yi
            if len(tdata) == 1:
                yi = 0
            trans.y = tdata[yi]
            if len(tdata) == 2:
                trans.x1 = x1
                trans.x2 = tdata[xi][1:-1]
            else:
                trans.x2 = None
            gr.transitions.append(trans)
    return gr

def SaveMooreMachineToCsv(moore: MooreMachine, filename: str):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')

        moore.states = sorted(moore.states, key=lambda state: not state.isStart)

        writer.writerow([''] + ['F' if s.isEnd else '' for s in moore.states])
        writer.writerow([''] + [s.state for s in moore.states])

        transition_data = {input_symbol: [] for input_symbol in moore.inputs}

        for input in moore.inputs:
            for state in moore.states:
                next_state = moore.transitions.get((state.state, input), '')
                transition_data[input].append(f"{','.join(next_state)}")

        for input in moore.inputs:
            row = [input] + transition_data[input]
            writer.writerow(row)

def ReadContent(path: str) -> str:
    with open(path) as f:
        return f.read()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some CSV files.')
    parser.add_argument('inputFile', type=str, help='Input txt')
    parser.add_argument('outputFile', type=str, help='Output csv')

    args = parser.parse_args()
    gr = ReadGramma(ReadContent(args.inputFile))
    mr = ConvertGrammarToMoore(gr)
    SaveMooreMachineToCsv(mr, args.outputFile)

