#!/usr/bin/env python

def readInput(fileName):
    """ Read a single line of comma-separated integers into an array."""

    with open(fileName) as f:
        firstLine = f.readlines()[0].split(",")

        return [int(i) for i in firstLine]


def restoreGravityAssistProgram(program):
    program[1] = 12
    program[2] = 2

    return program


def runIntcode(program):
    """Simulate an Intcode machine by processing an array of integers."""

    pc = 0

    while program[pc] != 99:
        command = program[pc]
        reg1 = program[program[pc + 1]]
        reg2 = program[program[pc + 2]]
        dest = program[pc + 3]

        if command == 1:
            print (pc, " (add) ", reg1, " ", reg2, " -> ", dest)
            program[dest] = reg1 + reg2

        if command == 2:
            print (pc, " (mul) ", reg1, " ", reg2, " -> ", dest)
            program[dest] = reg1 * reg2

        pc = pc + 4

    return program


def testIntcodeProgram():
    """Run sample I/O from AoC question 2.1"""

    testData = [
            {
                "input": [1, 0, 0, 0, 99],
                "output": [2, 0, 0, 0, 99]
            },
            {
                "input": [2, 3, 0, 3, 99],
                "output": [2, 3, 0, 6, 99]
            },
            {
                "input": [2, 4, 4, 5, 99, 0],
                "output": [2, 4, 4, 5, 99, 9801]
            },
            {
                "input": [1, 1, 1, 4, 99, 5, 6, 0, 99],
                "output": [30, 1, 1, 4, 2, 5, 6, 0, 99]
            },
        ]

    overallSuccess = True

    for test in testData:
        input = test['input']
        expectedResult = test['output']

        result = runIntcode(input.copy())

        if result == expectedResult:
            print ("Testing", input, "... ok")
        else:
            print ("Testing", input, "... fail, got ", result)
            overallSuccess = False

    return overallSuccess


def main():
    if not testIntcodeProgram():
        print("Tests failed.")
        exit()

    program = readInput("aoc-2.1.input")
    print ("Input: ", program)

    program = restoreGravityAssistProgram(program)
    print ("Restored: ", program)

    result = runIntcode(program)
    print ("Result: ", program)

    print(result[0])


if __name__ == "__main__":
    main()
