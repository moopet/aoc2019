#!/usr/bin/env python

class Path:
    def __init__(self):
       self.x = 0
       self.y = 0
       self.instructions = []
       self.points = []

    def processSingleInstruction(self, instruction):
        direction = instruction[0]
        distance = int(instruction[1:])

        while distance:
            if direction == "U":
                self.y = self.y - 1
            elif direction == "D":
                self.y = self.y + 1
            elif direction == "L":
                self.x = self.x - 1
            else:
                self.x = self.x + 1

            self.points.append([self.x, self.y])
            distance = distance - 1

    def readInstructions(self, fileName, line_number):
        """Read a line of comma-separated instructions into an array."""

        with open(fileName) as f:
            for current_line_number, line in enumerate(f):
                if current_line_number == line_number:
                    self.instructions = line.split(",")

    def setInstructions(self, instructions):
        """Load i string of nstructions for test purposes."""

        self.instructions = instructions.split(",")

    def processInstructions(self):
        for instruction in self.instructions:
            self.processSingleInstruction(instruction)


def testDay3():
    """Run sample I/O from AoC question 3.1"""

    testData = [
            {
                "input": [
                    "R75,D30,R83,U83,L12,D49,R71,U7,L72",
                    "U62,R66,U55,R34,D71,R55,D58,R83"
                ],
                "output": 159

            },
            {
                "input": [
                    "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
                    "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
                ],
                "output": 135
            },
        ]

    overallSuccess = True

    for test in testData:
        path1 = Path()
        path2 = Path()

        path1.setInstructions(test['input'][0])
        path1.processInstructions()

        path2.setInstructions(test['input'][1])
        path2.processInstructions()

        expectedResult = test['output']
        actualResult = getClosestCommonPoint(path1, path2)

        if actualResult == expectedResult:
            print ("Testing", input, "... ok")
        else:
            print ("Testing", input, "... fail: expected ", expectedResult, " got ", actualResult)
            overallSuccess = False

    return overallSuccess


def getCommonPoints(points1, points2):
    print ("Lengths: ", len(points1), ", ", len(points2))
    return [p for p in points1 if p in points2]


def getManhattanDistance(point):
    """Find the Manhattan distance of a point (x, y array) with respect to the origin."""
    return abs(point[0]) + abs(point[1])


def getClosestCommonPoint(path1, path2):
    common_points = getCommonPoints(path1.points, path2.points)
    distances = [getManhattanDistance(p) for p in common_points]

    return min(distances)


def main():
    if not testDay3():
        print("Tests failed.")
        exit()

    filename = "aoc-3.1.input"

    wire1 = Path()
    wire1.readInstructions(filename, 0)
    wire1.processInstructions()

    wire2 = Path()
    wire2.readInstructions(filename, 1)
    wire2.processInstructions()

    print ("natch")
    print ("Result: ", getClosestCommonPoint(wire1, wire2))


if __name__ == "__main__":
    main()
