from collections import deque
from typing import Set, Dict, List
from abc import ABC, abstractmethod


class MooreTransition:
    def __init__(self, fromState: int, toStates: Set[int], inSymbol: str):
        if toStates is None:
            toStates = set()
        self.fromState = fromState
        self.toStates = toStates
        self.inSymbol = inSymbol


class MooreState:
    def __init__(self, state: str = "", outSymbol: str = "", transitions: Set[int] = None):
        if transitions is None:
            transitions = set()
        self.state = state
        self.outSymbol = outSymbol
        self.transitions = transitions


class RegexToNFAConverter:
    def __init__(self, regularExpression: str):
        self.alphabet = {"ε"}
        self.states: List[MooreState] = []
        self.statesMap: Dict[str, int] = {}
        self.transitions: List[MooreTransition] = []
        self.regularExpression = regularExpression
        self.convert()

    def addTransitionImpl(self, fromState: int, toState: int, ch: str = "ε", needAddNewState: bool = False):
        if needAddNewState:
            self.states.append(MooreState(f"S{toState}", "", {len(self.transitions)}))
        self.states[fromState].transitions.add(len(self.transitions))
        self.transitions.append(MooreTransition(fromState, {toState}, ch))

    def addTransitionToNewState(self, fromState: int, toState: int, ch: str = "ε"):
        self.addTransitionImpl(fromState, toState, ch, True)

    def addTransitionToExistState(self, fromState: int, toState: int, ch: str = "ε"):
        self.addTransitionImpl(fromState, toState, ch, False)

    def writeResultToCsvFile(self, filename: str):
        with open(filename, 'w') as file:
            file.write(";".join([""] + [state.outSymbol for state in self.states]) + "\n")
            file.write(";".join([""] + [state.state for state in self.states]) + "\n")

            for inSymbol in self.alphabet:
                file.write(inSymbol)
                for state in self.states:
                    emptyTransitionsSet = set()
                    for transition in state.transitions:
                        t = self.transitions[transition]
                        if t.fromState != self.states.index(state) or t.inSymbol != inSymbol:
                            continue
                        for toState in t.toStates:
                            if toState == self.states.index(state) and inSymbol == "ε":
                                continue
                            emptyTransitionsSet.add(self.states[toState].state)

                    emptyTransitions = ",".join(emptyTransitionsSet)
                    file.write(f";{emptyTransitions}")
                file.write("\n")

    def convert(self):
        stateCounter = 0
        stateIndex = 0
        preBracketStateIndex = deque([0])
        stateIndexToBrackets = deque([set()])

        self.states.append(MooreState("S0"))
        self.transitions.append(MooreTransition(0, {0}, "ε"))

        isBracketClose = False
        isBracketOpen = False

        for c in self.regularExpression:
            state = getRegularState(c)
            [isBracketClose,
             isBracketOpen,
             stateCounter,
             stateIndex,
             preBracketStateIndex,
             stateIndexToBrackets] = state.To(
                self, isBracketClose, isBracketOpen,
                stateCounter, stateIndex, preBracketStateIndex, stateIndexToBrackets, c
            )

        stateCounter += 1
        self.states.append(MooreState(f"S{stateCounter}", "F"))
        if stateIndexToBrackets:
            stateIndexToBrackets[-1].add(stateIndex)

        if stateIndexToBrackets and stateIndexToBrackets[-1]:
            for stateInd in stateIndexToBrackets[-1]:
                self.addTransitionToExistState(stateInd, stateCounter)


class RegularState(ABC):
    @abstractmethod
    def To(self, converter: RegexToNFAConverter, isBracketClose: bool, isBracketOpen: bool, stateCounter: int,
           stateIndex: int, preBracketStateIndex: deque[int],
           stateIndexToBrackets: deque[set], c: str = ""):
        pass


def getRegularState(c: str) -> RegularState:
    if c == "|":
        return RegularStateOr()
    elif c == "(":
        return RegularStateOpen()
    elif c == ")":
        return RegularStateClose()
    elif c == "+":
        return RegularStatePlus()
    elif c == "*":
        return RegularStateMulti()
    else:
        return RegularStateDefault()


class RegularStateOr(RegularState):
    def To(self, converter: RegexToNFAConverter, isBracketClose: bool, isBracketOpen: bool, stateCounter: int,
           stateIndex: int, preBracketStateIndex: deque[int],
           stateIndexToBrackets: deque[set], c: str = ""):
        if isBracketClose:
            preBracketStateIndex.pop()

        stateIndexToBrackets[-1].add(stateIndex)
        stateIndex = preBracketStateIndex[-1]
        return [isBracketClose, isBracketOpen, stateCounter, stateIndex, preBracketStateIndex, stateIndexToBrackets]


class RegularStateOpen(RegularState):
    def To(self, converter: RegexToNFAConverter, isBracketClose: bool, isBracketOpen: bool, stateCounter: int,
           stateIndex: int, preBracketStateIndex: deque[int],
           stateIndexToBrackets: deque[set], c: str = ""):
        stateCounter += 1
        converter.states.append(MooreState(f"S{stateCounter}"))

        converter.addTransitionToExistState(stateCounter, stateCounter)
        converter.addTransitionToExistState(stateIndex, stateCounter)

        stateIndex = stateCounter
        stateIndexToBrackets.append(set())
        preBracketStateIndex.append(stateCounter)

        isBracketOpen = True
        isBracketClose = False
        return [isBracketClose, isBracketOpen, stateCounter, stateIndex, preBracketStateIndex, stateIndexToBrackets]


class RegularStateClose(RegularState):
    def To(self, converter: RegexToNFAConverter, isBracketClose: bool, isBracketOpen: bool, stateCounter: int,
           stateIndex: int, preBracketStateIndex: deque[int],
           stateIndexToBrackets: deque[set], c: str = ""):
        stateCounter += 1
        if isBracketOpen:
            converter.addTransitionToNewState(stateIndex, stateCounter)
            stateIndex = stateCounter
            preBracketStateIndex.pop()
            stateIndexToBrackets.pop()
        else:
            if isBracketClose:
                preBracketStateIndex.pop()

            converter.states.append(MooreState(f"S{stateCounter}"))
            converter.addTransitionToExistState(stateIndex, stateCounter)
            if stateIndexToBrackets[-1]:
                for stateInd in stateIndexToBrackets[-1]:
                    converter.addTransitionToExistState(stateInd, stateCounter)
            stateIndexToBrackets.pop()
            stateIndex = stateCounter
            isBracketClose = True
        isBracketOpen = False
        return [isBracketClose, isBracketOpen, stateCounter, stateIndex, preBracketStateIndex, stateIndexToBrackets]


class RegularStatePlus(RegularState):
    def To(self, converter: RegexToNFAConverter, isBracketClose: bool, isBracketOpen: bool, stateCounter: int,
           stateIndex: int, preBracketStateIndex: deque[int],
           stateIndexToBrackets: deque[set], c: str = ""):
        stateCounter += 1
        if isBracketClose:
            converter.addTransitionToNewState(stateIndex, stateCounter)
            transition = converter.transitions[next(iter(converter.states[preBracketStateIndex[-1]].transitions))]
            converter.addTransitionToExistState(stateCounter, preBracketStateIndex[-1], transition.inSymbol)
            preBracketStateIndex.pop()
        else:
            converter.addTransitionToNewState(stateIndex, stateCounter)
            transition = converter.transitions[next(iter(converter.states[stateIndex].transitions))]
            converter.addTransitionToExistState(stateCounter, stateIndex, transition.inSymbol)

        stateIndex = stateCounter
        isBracketOpen = False
        isBracketClose = False
        return [isBracketClose, isBracketOpen, stateCounter, stateIndex, preBracketStateIndex, stateIndexToBrackets]


class RegularStateMulti(RegularState):
    def To(self, converter: RegexToNFAConverter, isBracketClose: bool, isBracketOpen: bool, stateCounter: int,
           stateIndex: int, preBracketStateIndex: deque[int],
           stateIndexToBrackets: deque[set], c: str = ""):
        stateCounter += 1
        if isBracketClose:
            converter.addTransitionToNewState(stateIndex, stateCounter)
            transition = converter.transitions[next(iter(converter.states[preBracketStateIndex[-1]].transitions))]
            converter.addTransitionToExistState(stateIndex, preBracketStateIndex[-1], transition.inSymbol)
            converter.addTransitionToExistState(transition.fromState, stateCounter)
            preBracketStateIndex.pop()
        else:
            converter.addTransitionToNewState(stateIndex, stateCounter)
            transition = converter.transitions[next(iter(converter.states[stateIndex].transitions))]
            converter.addTransitionToExistState(stateCounter, stateIndex, transition.inSymbol)
            converter.addTransitionToExistState(transition.fromState, stateCounter)

        stateIndex = stateCounter
        isBracketOpen = False
        isBracketClose = False
        return [isBracketClose, isBracketOpen, stateCounter, stateIndex, preBracketStateIndex, stateIndexToBrackets]


class RegularStateDefault(RegularState):
    def To(self, converter: RegexToNFAConverter, isBracketClose: bool, isBracketOpen: bool, stateCounter: int,
           stateIndex: int, preBracketStateIndex: deque[int],
           stateIndexToBrackets: deque[set], c: str = ""):
        stateCounter += 1
        if isBracketClose:
            preBracketStateIndex.pop()

        converter.alphabet.add(c)
        converter.addTransitionToNewState(stateIndex, stateCounter, c)
        stateIndex = stateCounter
        isBracketOpen = False
        isBracketClose = False
        return [isBracketClose, isBracketOpen, stateCounter, stateIndex, preBracketStateIndex, stateIndexToBrackets]


if __name__ == "__main__":
    import sys

    if len(sys.argv) not in {3, 4}:
        print("main.py <outputFile> regularExpression")
        sys.exit(1)

    outputFile = sys.argv[1]
    regularExpression = sys.argv[2]

    if len(sys.argv) == 4:
        outputFile = sys.argv[2]
        regularExpression = sys.argv[3]

    rtNfa = RegexToNFAConverter(regularExpression)
    rtNfa.writeResultToCsvFile(outputFile)