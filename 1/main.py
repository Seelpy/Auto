import csv
import argparse

DEFAULT_MIN_STATE_NAME = 'X'
STATE_OUTPUT_SEPARATOR = '/'
STATE_INPUT_SEPARATOR = '/'
DEFAULT_GROUP_PREFIX = "_ "
MINIMIZE_MEALY = 'mealy'
MINIMIZE_MOORE = 'moore'

def writeToCsv(fileName, data, delimiter=';'):
    with open(fileName, 'w', newline='', encoding='ISO-8859-1') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows(data)

def readDataFromCsv(fileName):
    with open(fileName, 'r', encoding='ISO-8859-1') as file:
        reader = csv.reader(file, delimiter=";")
        data = []

        for row in reader:
            data.append(row)
    return data


def createMealyInputToTransitions(data, states):
    outputs = {}
    inputToTransitions = {}

    for transitions in data:
        inputValue = transitions[0].strip()

        for i, transition in enumerate(transitions[1:]):
            state, output = transition.strip().split(STATE_OUTPUT_SEPARATOR)

            if state not in outputs:
                outputs[state] = set()
            outputs[state].add(output.strip())

            if inputValue not in inputToTransitions:
                inputToTransitions[inputValue] = {}

            inputToTransitions[inputValue][states[i]] = f"{state}{STATE_OUTPUT_SEPARATOR}{output}"

    return inputToTransitions

def readMealyFromCsv(fileName):
    data = readDataFromCsv(fileName)

    states = [state.strip() for state in data[0][1:]]

    inputToTransitions = createMealyInputToTransitions(data[1:], states)
    return states, inputToTransitions


def createMooreInputToTransitions(data, states, outputs):
    inputToTransitions = {}

    for transitions in data:
        inputValue = transitions[0].strip()

        for i, transition in enumerate(transitions[1:]):
            nextState = transition.strip()
            currentState = states[i]
            output = outputs[currentState]

            if inputValue not in inputToTransitions:
                inputToTransitions[inputValue] = {}

            inputToTransitions[inputValue][currentState] = f"{nextState}{STATE_OUTPUT_SEPARATOR}{output}"
    return inputToTransitions

def readMooreFromCsv(fileName):
    data = readDataFromCsv(fileName)

    outputs = data[0][1:]
    states = data[1][1:]

    mooreStates = []
    mooreStateOutputs = {}

    for output, state in zip(outputs, states):
        mooreStates.append(state.strip())
        mooreStateOutputs[state.strip()] = output.strip()

    inputToTransitions = createMooreInputToTransitions(data[2:], mooreStates, mooreStateOutputs)

    return mooreStates, inputToTransitions

def splitStatesInGroup(states, inputValueToTransitions, prevStateToGroup=None):
    groups = {}
    groupOutputs = {}
    stateToGroup = {}

    def splitStates(state, groupPrefix=DEFAULT_GROUP_PREFIX):
        groupInputs = [groupPrefix]
        outputs = []
        for inputValue in inputValueToTransitions:
            if prevStateToGroup is None:
                groupInput = inputValueToTransitions[inputValue][state].split(STATE_INPUT_SEPARATOR)[1]
                groupInputs.append(groupInput)
                continue

            groupInput = inputValueToTransitions[inputValue][state].split(STATE_INPUT_SEPARATOR)[0]
            outputs.append(inputValueToTransitions[inputValue][state].split(STATE_INPUT_SEPARATOR)[1])

            groupName = prevStateToGroup[groupInput]
            groupInput = list(dict.fromkeys(prevStateToGroup.values())).index(groupName)
            groupInputs.append(str(groupInput))

        groupInputsStr = ' '.join(groupInputs)

        if groupInputsStr not in groups.keys():
            groups[groupInputsStr] = []
        groups[groupInputsStr].append(state)
        groupOutputs[groupInputsStr] = outputs
        stateToGroup[state] = groupInputsStr

    if isinstance(states, list):
        for state in states:
            splitStates(state)
    else:
        for i, group in enumerate(states, start=1):
            for state in states[group]:
                splitStates(state, f'\{i}')

    return groups, groupOutputs, stateToGroup


def groupStatesToInputs(states, inputValueToTransitions):
    groups, _, stateToGroup = splitStatesInGroup(states, inputValueToTransitions)
    groups, _, stateToGroup = splitStatesInGroup(groups, inputValueToTransitions, stateToGroup)

    while True:
        newGroups, groupOutputs, stateToGroup = splitStatesInGroup(groups, inputValueToTransitions, stateToGroup)
        isEqual = str(newGroups) == str(groups)
        groups = newGroups

        if isEqual:
            break

    return groups, groupOutputs


def getStatesFromGroups(groups):
    statesRow = ['']
    for i in range(len(groups)):
        state = DEFAULT_MIN_STATE_NAME + str(i)
        statesRow.append(state)
    return statesRow

def getOutputsFromGroups(groupOutputs, groups):
    outputsRow = ['']
    for i in range(len(groups)):
        output = groupOutputs[list(groups.keys())[i]][0]
        outputsRow.append(output)
    return outputsRow

def generateTransitionsRows(inputValueToTransitions, groups, groupOutputs = None):
    transitionsRows = []
    for i, inputValue in enumerate(inputValueToTransitions):
        row = [inputValue]
        for group in groups:
            groupStates = group.split(' ')[1:]
            state = DEFAULT_MIN_STATE_NAME + str(groupStates[i])
            if groupOutputs != None:
                output = groupOutputs[group][i]
                transition = state + STATE_INPUT_SEPARATOR + output
            else:
                transition = DEFAULT_MIN_STATE_NAME + str(groupStates[i])
            row.append(transition)

        transitionsRows.append(row)
    return transitionsRows


def minimizeMealy(inputFileName, outputFileName):
    mealyStates, inputValueToTransitions = readMealyFromCsv(inputFileName)
    groups, groupOutputs = groupStatesToInputs(mealyStates, inputValueToTransitions)

    statesRow = getStatesFromGroups(groups)

    transitionsRows = generateTransitionsRows(inputValueToTransitions, groups, groupOutputs)

    data = [statesRow]
    for transitionRow in transitionsRows:
        data.append(transitionRow)

    writeToCsv(outputFileName, data)


def minimizeMoore(inputFileName, outputFileName):
    mooreStates, inputValueToTransitions = readMooreFromCsv(inputFileName)
    groups, groupOutputs = groupStatesToInputs(mooreStates, inputValueToTransitions)

    outputsRow = getOutputsFromGroups(groupOutputs, groups)
    statesRow = getStatesFromGroups(groups)

    transitionsRows = generateTransitionsRows(inputValueToTransitions, groups)

    data = [outputsRow, statesRow]
    for transitionRow in transitionsRows:
        data.append(transitionRow)

    writeToCsv(outputFileName, data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some CSV files.')
    parser.add_argument('command', type=str, help='Input CSV file for Mealy')
    parser.add_argument('inputFileName', type=str, help='Input CSV file')
    parser.add_argument('outputFileName', type=str, help='Output CSV file')

    args = parser.parse_args()

    if args.command == MINIMIZE_MEALY:
        minimizeMealy(args.inputFileName, args.outputFileName)
    elif args.command == MINIMIZE_MOORE:
        minimizeMoore(args.inputFileName, args.outputFileName)