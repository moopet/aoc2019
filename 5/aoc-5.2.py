#!/usr/bin/env python

import sys
import ipdb
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
        print (program)
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
    """Run sample I/O from AoC question 2.1"""

    tests = [
            {
                "name": "set/get",
                "program": [3, 0, 4, 0, 99],
                "input": [123],
                "output": [123]
            },
            {
                "name": "multiply/exit",
                "program": [1002, 4, 3, 4, 33],
                "input": [],
                "output": []
            },
            {
                "name": "non-zero/positional",
                "program": [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
                "input": [0],
                "output": [0]
            },
            {
                "name": "non-zero/positional",
                "program": [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
                "input": [1],
                "output": [1]
            },
            {
                "name": "non-zero/positional",
                "program": [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
                "input": [-1],
                "output": [1]
            },
            {
                "name": "non-zero/immediate",
                "program": [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1],
                "input": [0],
                "output": [0]
            },
            {
                "name": "non-zero/immediate",
                "program": [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1],
                "input": [1],
                "output": [1]
            },
            {
                "name": "non-zero/immediate",
                "program": [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1],
                "input": [-1],
                "output": [1]
            },
            {
                "name": "equal/positional",
                "program": [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8],
                "input": [8],
                "output": [1]
            },
            {
                "name": "equal/positional",
                "program": [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8],
                "input": [7],
                "output": [0]
            },
            {
                "name": "less-than/positional",
                "program": [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8],
                "input": [7],
                "output": [1]
            },
            {
                "name": "less-than/positional",
                "program": [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8],
                "input": [9],
                "output": [0]
            },
            {
                "name": "equal/immediate",
                "program": [3, 3, 1108, -1, 8, 3, 4, 3, 99],
                "input": [8],
                "output": [1]
            },
            {
                "name": "equal/immediate",
                "program": [3, 3, 1108, -1, 8, 3, 4, 3, 99],
                "input": [18],
                "output": [0]
            },
            {
                "name": "less-than/immediate",
                "program": [3, 3, 1107, -1, 8, 3, 4, 3, 99],
                "input": [5],
                "output": [1]
            },
            {
                "name": "less-than/immediate",
                "program": [3, 3, 1107, -1, 8, 3, 4, 3, 99],
                "input": [8],
                "output": [0]
            },
            {
                "name": "less-than",
                "program": [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99],
                "input": [5],
                "output": [999]
            },
            {
                "name": "equal",
                "program": [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99],
                "input": [8],
                "output": [1000]
            },
            {
                "name": "greater-than",
                "program": [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99],
                "input": [18],
                "output": [1001]
            },
        ]

    overallSuccess = True

    for test in tests:
        print ("Testing ", test["name"])
        print ("runIntcode(", test["program"], ", ", test["input"], ") == ", test["output"], sep="")

        try:
            output = runIntcode(test["program"], test["input"])
        except IndexError:
            output = "IndexError exception"

        if output == test["output"]:
            print ("Pass")
        else:
            print ("Fail: got ", output)
            overallSuccess = False
            exit()

        print ("--")

    return overallSuccess


def main():
    if not testIntcodeProgram():
        print("Tests failed.")
        exit()

    print ("Tests passed.")

    program = readInput("aoc-5.1.input")
    result = runIntcode(program, [5])
    print ("Result: ", result)


if __name__ == "__main__":
    main()
