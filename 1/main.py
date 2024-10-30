import csv
import argparse

NEW_STATE_NAME = 'q'
STATE_OUTPUT_SEPARATOR = '/'
CONVERT_TYPE_MEALY_TO_MOORE = 'mealy-to-moore'
CONVERT_TYPE_MOORE_TO_MEALY = 'moore-to-mealy'

def printFormattedDict(data):
    for row in data:
        formattedRow = " ".join(f"{item:<7}" for item in row)
        print(formattedRow)
    print()


def writeToCsv(fileName, data, delimiter=';'):
    with open(fileName, 'w', newline='', encoding='ISO-8859-1') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows(data)

def readMealyFromCsv(fileName, delimiter=';'):
    with open(fileName, 'r', encoding='ISO-8859-1') as file:
        reader = csv.reader(file, delimiter=delimiter)
        data = []

        for row in reader:
            data.append(row)

        printFormattedDict(data)

        mealyStates = []
        for index, state in enumerate(data[0]):
            if index == 0:
                continue
            mealyStates.append(state.strip())

        mealyStateOutputs = {}
        inputValueToTransitions = {}
        for index, transitions in enumerate(data):
            if index == 0:
                continue

            inputValue = transitions[0].strip()

            for index2, transition in enumerate(transitions[1:]):
                state = transition.strip().split(STATE_OUTPUT_SEPARATOR)[0]
                output = transition.strip().split(STATE_OUTPUT_SEPARATOR)[1]

                if state not in mealyStateOutputs:
                    mealyStateOutputs[state] = set()
                mealyStateOutputs[state].add(output)

                if inputValue not in inputValueToTransitions:
                    inputValueToTransitions[inputValue] = {}
                    inputValueToTransitions[inputValue][mealyStates[index2]] = {}

                inputValueToTransitions[inputValue][mealyStates[index2]] = state + STATE_OUTPUT_SEPARATOR + output

        return mealyStates, mealyStateOutputs, inputValueToTransitions


def readMooreFromCsv(fileName, delimiter=';'):
    with open(fileName, 'r', encoding='ISO-8859-1') as file:
        reader = csv.reader(file, delimiter=delimiter)
        data = []

        for row in reader:
            data.append(row)

        printFormattedDict(data)

        outputs = []
        for index, output in enumerate(data[0]):
            if index == 0:
                continue

            outputs.append(output.strip())

        mooreStates = []
        for index, mooreState in enumerate(data[1]):
            if index == 0:
                continue

            mooreStates.append(mooreState.strip())

        mooreStateOutputs = {}
        for index, mooreState in enumerate(mooreStates):
            output = outputs[index]
            mooreStateOutputs[mooreState] = output

        inputValueToTransitions = {}
        for index, transitions in enumerate(data):
            if index <= 1:
                continue

            inputValue = transitions[0].strip()

            for index2, transition in enumerate(transitions[1:]):
                state = transition.strip()
                output = mooreStateOutputs[state]

                if inputValue not in inputValueToTransitions:
                    inputValueToTransitions[inputValue] = {}

                mooreState = list(mooreStateOutputs.keys())[index2]
                inputValueToTransitions[inputValue][mooreState] = state + STATE_OUTPUT_SEPARATOR + output

        return mooreStateOutputs, inputValueToTransitions


def mealyToMoore(mealyStates, mealyStateOutputs, inputValueToTransitions):
    mealyToMooreStates = {}

    mealyStateOutputs = dict(
        sorted(mealyStateOutputs.items(),
               key=lambda item: mealyStates.index(item[0]) if item[0] in mealyStates else float('inf')))
    for mealyState, output in mealyStateOutputs.items():
        mealyStateOutputs[mealyState] = sorted(output)

    for mealyState in mealyStates:
        if mealyState in mealyStateOutputs:
            for output in mealyStateOutputs[mealyState]:
                transition = mealyState + STATE_OUTPUT_SEPARATOR + output
                mealyToMooreStates[transition] = NEW_STATE_NAME + str(len(mealyToMooreStates))
        else:
            mealyToMooreStates[mealyState] = NEW_STATE_NAME + str(len(mealyToMooreStates))

    outputsRow = ['']
    statesRow = ['']
    for mealyState in mealyStates:
        if mealyState in mealyStateOutputs:
            for output in mealyStateOutputs[mealyState]:
                outputsRow.append(output)
                statesRow.append(mealyToMooreStates[mealyState + STATE_OUTPUT_SEPARATOR + output])
        else:
            outputsRow.append('')
            statesRow.append(mealyToMooreStates[mealyState])

    transitionsRows = []
    for inputValue, transitions in inputValueToTransitions.items():
        row = [inputValue]

        for currentState in transitions:
            nextState = inputValueToTransitions[inputValue][currentState]

            countOutputs = len(mealyStateOutputs.get(currentState, [1]))
            for i in range(countOutputs):
                row.append(mealyToMooreStates[nextState])

        transitionsRows.append(row)

    data = [outputsRow, statesRow]
    for transitionRow in transitionsRows:
        data.append(transitionRow)

    return data


def mooreToMealy(mooreStateOutputs, inputValueToTransitions):
    statesRow = ['']
    for mooreState in mooreStateOutputs.keys():
        statesRow.append(mooreState)

    transitionsRows = []
    for inputValue, transitions in inputValueToTransitions.items():
        row = [inputValue]

        for currentState in transitions:
            nextState = inputValueToTransitions[inputValue][currentState]
            row.append(nextState)

        transitionsRows.append(row)

    data = [statesRow]
    for transitionRow in transitionsRows:
        data.append(transitionRow)

    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some CSV files.')
    parser.add_argument('conertType', type=str, help='Input CSV file for Mealy')
    parser.add_argument('inputFileName', type=str, help='Input CSV file')
    parser.add_argument('outputFileName', type=str, help='Output CSV file')

    args = parser.parse_args()

    if args.conertType == CONVERT_TYPE_MEALY_TO_MOORE:
        writeToCsv(args.outputFileName, mealyToMoore(*readMealyFromCsv(args.inputFileName)))
    elif args.conertType == CONVERT_TYPE_MOORE_TO_MEALY:
        writeToCsv(args.outputFileName, mooreToMealy(*readMooreFromCsv(args.inputFileName)))
    else:
        print('Not found')
