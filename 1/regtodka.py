import regtonka
import nkatodka
import csv
import os
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
        self.expression = expression
        regexToNFACovnerter = regtonka.RegexToNFAConverter(expression)
        try:
            os.remove("./data/nka.csv")
            os.remove("./data/dka.csv")
        except OSError as e:
            print(f"Error deleting files: {e}")

        regexToNFACovnerter.writeResultToCsvFile("./data/nka.csv")
        nkatodka.determine_nfa("./data/nka.csv", "./data/dka.csv")
        data = self.readDKAFromCSV("./data/dka.csv")
        return data
    def readDKAFromCSV(self, path: str) -> slider.Slider:
        data = readDataFromCsv(path)

        outputs = data[0][1:]
        states = data[1][1:]
        finishStates = []

        mooreStates: list[slider.State] = []

        for output, state in zip(outputs, states):
            mooreStates.append(slider.State(state))
            if output == "F":
                finishStates.append(state)

        for transitions in data[2:]:
            input = transitions[0]

            for i, transition in enumerate(transitions[1:]):
                if transition != "":
                    if i >= len(mooreStates):
                        print(i)
                    mooreStates[i].AddTransition(input, transition)

        return slider.Slider(mooreStates, finishStates)
