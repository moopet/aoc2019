#!/usr/bin/env python

import sys
import ipdb
from itertools import permutations
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=1)

def readInput(fileName):
    """ Read a single line of comma-separated integers into an array."""

    with open(fileName) as f:
        firstLine = f.readlines()[0].split(",")

        return [int(i) for i in firstLine]


def getParameterModes(opcode):
    """
    Unpack parameter modes from a single integer.

    True: Immediate
    False: Positional
    """

    opcode = int(opcode / 100)
    modes = []

    for i in range(3):
       modes.append(True if opcode % 10 else False)
       opcode = int(opcode / 10)

    #print ("Unpack modes: ", opcode, " -> ", modes)

    return modes


def getParameters(program, ip, number_of_parameters, modes):
    parameters = []

    opcode = program[ip]
    address = ip + 1

    for i in range(number_of_parameters):
        value = program[address]

        if not modes[i]:
            value = program[value]

        parameters.append(value)
        address = address + 1

    return parameters


def runIntcode(program, inputs):
    """Simulate an Intcode machine by processing an array of integers."""

    ip = 0
    output = []
    inputs.reverse() # So we can use .pop() later.

    while program[ip] != 99:
        opcode_with_parameter_modes = program[ip]

        modes = getParameterModes(opcode_with_parameter_modes)
        opcode = opcode_with_parameter_modes % 100

        if opcode == 1:
            """Add."""

            parameters = getParameters(program, ip, 2, modes)
            dest = program[ip + 3]
            #print (ip, " (add) ", parameters[0], " ", parameters[1], " -> ", dest)

            program[dest] = parameters[0] + parameters[1]

            ip = ip + 4

        if opcode == 2:
            """Multiply."""

            parameters = getParameters(program, ip, 2, modes)
            dest = program[ip + 3]
            #print (ip, " (mul) ", parameters[0], " ", parameters[1], " -> ", dest)

            program[dest] = parameters[0] * parameters[1]

            ip = ip + 4

        if opcode == 3:
            """Input."""

            dest = program[ip + 1]
            #print (ip, " (inp) ", dest, inputs[-1])

            program[dest] = inputs.pop()

            ip = ip + 2

        if opcode == 4:
            """Output."""

            parameters = getParameters(program, ip, 1, modes)
            output.append(parameters[0])
            #print (ip, " (out) ", output[-1])

            ip = ip + 2

        if opcode == 5:
            """Jump if true."""

            parameters = getParameters(program, ip, 2, modes)

            if parameters[0] != 0:
                ip = parameters[1]
            else:
                ip = ip + 3

        if opcode == 6:
            """Jump if false."""

            parameters = getParameters(program, ip, 2, modes)

            if parameters[0] == 0:
                ip = parameters[1]
            else:
                ip = ip + 3

        if opcode == 7:
            """Set if less than."""

            parameters = getParameters(program, ip, 2, modes)
            dest = program[ip + 3]

            program[dest] = 1 if parameters[0] < parameters[1] else 0

            ip = ip + 4

        if opcode == 8:
            """Set if equal."""

            parameters = getParameters(program, ip, 2, modes)
            dest = program[ip + 3]

            program[dest] = 1 if parameters[0] == parameters[1] else 0

            ip = ip + 4

    return output


def testIntcodeProgram():
    """Run sample I/O from AoC question 7.1"""

    tests = [
            {
                "program": [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],
                "input": [4, 3, 2, 1, 0],
                "output": 43210
            },
            {
                "program": [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0],
                "input": [0, 1, 2, 3, 4],
                "output": 54321
            },
            {
                "program": [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0],
                "input": [1, 0, 4, 3, 2],
                "output": 65210
            }
        ]

    overallSuccess = True

    for test in tests:
        print ("runAmplifierCombination(", test["program"], ", ", test["input"], ") == ", test["output"], sep="")

        try:
            signal = runAmplifierCombination(test["program"], test["input"])
        except IndexError:
            signal = "IndexError exception"

        if signal == test["output"]:
            print ("Pass")
        else:
            print ("Fail: got ", signal)
            overallSuccess = False
            exit()

        print ("--")

    return overallSuccess


def runAmplifierCombination(program, sequence):
    signal = 0

    for x in range(5):
        phase = sequence[0]
        sequence = sequence[1:]

        output = runIntcode(program.copy(), [phase, signal])
        signal = output[0]

    print ("Sequence", sequence, ":", signal)
    return signal


def main():
    if not testIntcodeProgram():
        print("Tests failed.")
        exit()

    print ("Tests passed.")

    program = readInput("aoc-7.1.input")
    sequences = list(permutations(range(5)))

    signals = [runAmplifierCombination(program, sequence) for sequence in sequences]

    print ("Result: ", max(signals))


if __name__ == "__main__":
    main()
