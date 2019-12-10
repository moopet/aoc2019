#!/usr/bin/env python

import sys
import ipdb
from IPython.core import ultratb
from math import sqrt
sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=1)


class AsteroidField:
    """Grid representation of an asteroid field."""

    def __init__(self):
        self.reset()


    def reset(self):
        """Reset the program to the beginning, clearing queues."""

        self.map = []
        self.width = 0
        self.height = 0


    def set_map(self, map_):
        self.reset()

        for line in map_:
            self.map.append([x == "#" for x in line.strip()])

        self.width = len(self.map)
        self.height = len(self.map[0])


    def load_map_from_file(self, filename):
        """Read a series of lines of symbols into an array."""

        with open(filename) as f:
            for line in f.readlines():
                self.map.append([x == "#" for x in line.strip()])

        self.width = len(self.map)
        self.height = len(self.map[0])


    def print(self):
        for line in self.map:
            print ("".join(["#" if x else "." for x in line]))


    def get_delta(self, start, end):
        return {
            "x": end["x"] - start["x"],
            "y": end["y"] - start["y"]
        }


    def is_asteroid(self, point):
        return self.map[point["y"]][point["x"]]


    def get_distance(self, point1, point2):
        return sqrt((abs(point1["x"] - point2["x"]) ** 2) + (abs(point1["y"] - point2["y"]) ** 2))


    def is_between(self, start, end, point):
        if start == end or point in [start, end]:
            return False

        if self.get_distance(start, end) < self.get_distance(start, point):
            return False

        cross_product = (point["y"] - start["y"]) * (end["x"] - start["x"]) - (point["x"] - start["x"]) * (end["y"] - start["y"])
        # print(start, end, point, cross_product)

        return cross_product == 0


    def get_asteroids(self):
        points = []

        for y in range(self.height):
            for x in range(self.width):
                point = {
                    "x": x,
                    "y": y
                }

                if self.is_asteroid(point):
                    points.append(point)

        return points


    def get_visibility_score(self, potential_station):
        """
        Find how many asteroids have direct line of sight to the potential
        monitoring station.
        """

        score = 0

        for target_asteroid in self.get_asteroids():
            blocked = False

            for blocking_asteroid in self.get_asteroids():
                if self.is_between(potential_station, target_asteroid, blocking_asteroid):
                    blocked = True
                    # print ("Blocker", potential_station, target_asteroid, blocking_asteroid)
                    break

            if not blocked:
                score += 1

        return score


    def get_best_score(self):
        scores = []
        asteroids = self.get_asteroids()

        for potential_station in asteroids:
            score = self.get_visibility_score(potential_station)
            scores.append(score)
            #print (potential_station, score)

        return max(scores)


    def get_best_candidate_station(self):
        scores = []
        asteroids = self.get_asteroids()

        for potential_station in asteroids:
            scores.append(self.get_visibility_score(potential_station))

        return asteroids[scores.index(max(scores))]


def testAsteroidField():
    """Run sample I/O from AoC questions"""

    tests = [
        {
            "map": [
                ".#..#",
                ".....",
                "#####",
                "....#",
                "...##"
            ],
            "point": {"x": 3, "y": 4},
            "score": 8
        },
        {
            "map": [
                "......#.#.",
                "#..#.#....",
                "..#######.",
                ".#.#.###..",
                ".#..#.....",
                "..#....#.#",
                "#..#....#.",
                ".##.#..###",
                "##...#..#.",
                ".#....####"
            ],
            "point": {"x": 5, "y": 8},
            "score": 33
        },
        {
            "map": [
                "#.#...#.#.",
                ".###....#.",
                ".#....#...",
                "##.#.#.#.#",
                "....#.#.#.",
                ".##..###.#",
                "..#...##..",
                "..##....##",
                "......#...",
                ".####.###."
            ],
            "point": {"x": 1, "y": 2},
            "score": 35
        },
        {
            "map": [
                ".#..#..###",
                "####.###.#",
                "....###.#.",
                "..###.##.#",
                "##.##.#.#.",
                "....###..#",
                "..#.#..#.#",
                "#..#.#.###",
                ".##...##.#",
                ".....#.#.."
            ],
            "point": {"x": 6, "y": 3},
            "score": 41
        },
        {
            "map": [
                ".#..##.###...#######",
                "##.############..##.",
                ".#.######.########.#",
                ".###.#######.####.#.",
                "#####.##.#.##.###.##",
                "..#####..#.#########",
                "####################",
                "#.####....###.#.#.##",
                "##.#################",
                "#####.##.###..####..",
                "..######..##.#######",
                "####.##.####...##..#",
                ".#####..#.######.###",
                "##...#.##########...",
                "#.##########.#######",
                ".####.#.###.###.#.##",
                "....##.##.###..#####",
                ".#.#.###########.###",
                "#.#.#.#####.####.###",
                "###.##.####.##.#..##",
            ],
            "point": {"x": 11, "y": 13},
            "score": 210
        }
    ]

    overall_success = True

    for test in tests:
        machine = AsteroidField()
        machine.set_map(test['map'])
        score = machine.get_best_score()
        point = machine.get_best_candidate_station()

        if score == test["score"] and point == test["point"]:
            print ("Pass")
        else:
            print ("Fail: got ", point, " for ", score)
            print ("Expected ", test["point"], " for ", test["score"])
            overall_success = False

        print ("--")

    return overall_success


def main():
    if not testAsteroidField():
        print("AsteroidField tests failed.")
        exit()

    print ("Tests passed.")

    machine = AsteroidField()
    machine.load_map_from_file("aoc-10.1.input")
    machine.print()
    result = machine.get_best_candidate_station()

    print("Best station at", result)


if __name__ == "__main__":
    main()
