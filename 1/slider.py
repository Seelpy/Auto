class State:
    def __init__(self, name: str):
        self.name: str = name
        self.transitions: dict[str, str] = {}

    def AddTransition(self, input_value: str, next_state_name: str) -> None:
        self.transitions[input_value] = next_state_name

    def __str__(self) -> str:
        return self.name


class Slider:
    def __init__(self, states: list[State]):
        self.states: dict[str, State] = {state.name: state for state in states}
        self.initialState: State = states[0]
        self.currentState: State = states[0]
        self.outputString: str = ""

    def Move(self, input_value: str) -> None:
        if input_value in self.currentState.transitions.keys():
            next_state_name = self.currentState.transitions[input_value]
            self.currentState = self.states[next_state_name]
            self.outputString += input_value
        else:
            print("SDASD")
            raise ValueError()
    def IsFinal(self) -> bool:
        return len(self.currentState.transitions) == 0

    def GetOutputString(self) -> str:
        return self.outputString

    def Reset(self) -> None:
        self.currentState = self.initialState
        self.outputString = ""
