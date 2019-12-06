#!/usr/bin/env python

import sys
import ipdb
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=1)

def readInput(fileName):
    """Read an orbit map into an array."""

    orbits = {}

    with open(fileName) as f:
        for line in f.readlines():
            components = line.strip().split(")")
            orbits[components[1]] = components[0]

    return orbits


def runOrbitProgram(orbits):
    """Count the total number of orbits in an orbit map."""
    total = 0;

    for body in orbits:
        x = body

        while x in orbits:
            total = total + 1
            x = orbits[x]

    return total


def getOrbitsForSingleBody(orbits, body):
    path = []

    while body in orbits:
        path.append(orbits[body])
        body = orbits[body]

    return path


def getTransferPath(orbits, body1, body2):
    path1 = getOrbitsForSingleBody(orbits, body1)
    path2 = getOrbitsForSingleBody(orbits, body2)

    for body in path1:
        if body in path2:
            return path1.index(body) + path2.index(body)

    return None


def testOrbitProgram():
    """Run sample I/O from AoC question 2.1"""

    tests = [
            {
                "input": {
                    "B": "COM",
                    "C": "B",
                    "D": "C",
                    "E": "D",
                    "F": "E",
                    "G": "B",
                    "H": "G",
                    "I": "D",
                    "J": "E",
                    "K": "J",
                    "L": "K",
                    "YOU": "K",
                    "SAN": "I"
                    },
                "output": 4
                },
            ]

    overallSuccess = True

    for test in tests:
        output = getTransferPath(test['input'], 'YOU', 'SAN')

        if output == test['output']:
            print ("Testing", test['input'], "... ok")
        else:
            print ("Testing", test['input'], "... fail, expected ", test['output'], " got ", output)
            overallSuccess = False

    return overallSuccess


def main():
    if not testOrbitProgram():
        print("Tests failed.")
        exit()

    print ("Tests passed.")

    orbits = readInput("aoc-6.1.input")
    result = getTransferPath(orbits, 'YOU', 'SAN')

    print ("Result: ", result)


if __name__ == "__main__":
    main()
