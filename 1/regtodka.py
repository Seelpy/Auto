import regtonka
import nkatodka
import csv

import slider

STATE_OUTPUT_SEPARATOR = '/'

def readDataFromCsv(fileName) -> list[str]:
    with open(fileName, 'r', encoding='ISO-8859-1') as file:
        reader = csv.reader(file, delimiter=";")
        data = []

        for row in reader:
            data.append(row)
    return data

class RegToDKAConverter:
    def __init__(self):
        pass
    def convert(self, expression: str) -> slider.Slider:
        regexToNFACovnerter = regtonka.RegexToNFAConverter(expression)
        regexToNFACovnerter.writeResultToCsvFile("./data/nka.csv")
        nkatodka.determine_nfa("./data/nka.csv", "./data/dka.csv")
        return self.readDKAFromCSV("./data/dka.csv")
    def readDKAFromCSV(self, path: str) -> slider.Slider:
        data = readDataFromCsv(path)

        outputs = data[0][1:]
        states = data[1][1:]

        mooreStates: list[slider.State] = []

        for output, state in zip(outputs, states):
            mooreStates.append(slider.State(state))

        for transitions in data[2:]:
            input = transitions[0]

            for i, transition in enumerate(transitions[1:]):
                if transition != "":
                    mooreStates[i].AddTransition(input, transition)

        return slider.Slider(mooreStates)

class DKA:
    def __init__(self):
        pass

    def Find(self, string: str, start: int, end: int) -> str:
        pass