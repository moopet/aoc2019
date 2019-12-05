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

    print ("Unpack modes: ", opcode, " -> ", modes)

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
            print (ip, " (add) ", parameters[0], " ", parameters[1], " -> ", dest)

            program[dest] = parameters[0] + parameters[1]

            ip = ip + 4

        if opcode == 2:
            """Multiply."""

            parameters = getParameters(program, ip, 2, modes)
            dest = program[ip + 3]
            print (ip, " (mul) ", parameters[0], " ", parameters[1], " -> ", dest)

            program[dest] = parameters[0] * parameters[1]

            ip = ip + 4

        if opcode == 3:
            """Input."""

            dest = program[ip + 1]
            print (ip, " (inp) ", dest, inputs[-1])

            program[dest] = inputs.pop()

            ip = ip + 2

        if opcode == 4:
            """Output."""

            parameters = getParameters(program, ip, 1, modes)
            output.append(parameters[0])
            print (ip, " (out) ", output[-1])

            ip = ip + 2

    return output


def testIntcodeProgram():
    """Run sample I/O from AoC question 2.1"""

    tests = [
            {
                "program": [3, 0, 4, 0, 99],
                "input": [123],
                "output": [123]
            },
            {
                "program": [1002, 4, 3, 4, 33],
                "input": [],
                "output": []
            },
        ]

    overallSuccess = True

    for test in tests:
        output = runIntcode(test['program'], test['input'])

        if output == test['output']:
            print ("Testing", test['input'], "... ok")
        else:
            print ("Testing", test['input'], "... fail, expected ", test['output'], " got ", output)
            overallSuccess = False

    return overallSuccess


def main():
    if not testIntcodeProgram():
        print("Tests failed.")
        exit()

    print ("Tests passed.")

    program = readInput("aoc-5.1.input")
    result = runIntcode(program, [1])
    print ("Result: ", result)


if __name__ == "__main__":
    main()
