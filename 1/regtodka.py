import regtonka
import nkatodka
import mindka
import slider

from typing import List

class RegToDKAConverter:
    def __init__(self):
        pass
    def convert(self, expression: str) -> slider.Slider:
        nfa = regtonka.process_regex(expression)
        dfa = nkatodka.process_nfa(*nfa)
        states, input_symbols, transitions, outputs, initial_state = mindka.process_dfa(*dfa)

        sliderStates: List[slider.State] = [slider.State(initial_state)]
        finishStates = []

        for state in states:
            if outputs[state] == "F":
                finishStates.append(state)
            if state != initial_state:
                sliderState = slider.State(state)
                sliderStates.append(sliderState)
            else:
                sliderState = sliderStates[0]

            stateTransaction = transitions[state]
            for input_symbol in input_symbols:
                transaction = stateTransaction[input_symbol]
                if transaction:
                    sliderState.AddTransition(input_symbol, transaction)

        return slider.Slider(sliderStates, finishStates)
