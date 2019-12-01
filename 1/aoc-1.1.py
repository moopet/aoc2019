#!/usr/bin/env python

def calculateFuel(fileName):
  with open(fileName) as f:
    masses =  map(int, f.readlines())

  fuelRequirements = map(lambda x: int(x / 3) - 2, masses)

  return sum(fuelRequirements)

def main():
  print(calculateFuel('aoc-1.1.input'))

if __name__ == "__main__":
    main()
