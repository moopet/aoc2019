#!/usr/bin/env python

def calculateFuelForMass(mass):
  fuelMass = int(mass / 3) - 2

  if fuelMass > 0:
    fuelMass = fuelMass + calculateFuelForMass(fuelMass)

  return fuelMass if fuelMass > 0 else 0

def calculateFuel(fileName):
  with open(fileName) as f:
    masses =  map(int, f.readlines())

  fuelRequirements = map(calculateFuelForMass, masses)

  return sum(fuelRequirements)

def main():
  print(calculateFuel('aoc-1.1.input'))

if __name__ == "__main__":
    main()
