#!/usr/bin/env python

import sys
import ipdb
from itertools import permutations
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=1)


class IntcodeInputError(Exception):
    """An error with the input queue for an Intcode machine."""

    pass


class IntcodeError(Exception):
    """A generic error with an Intcode machine."""

    pass


class IntcodeMachine:
    """Intcode machine emulator."""

    def __init__(self, name = None, verbose = False, debugging = False):
        self.verbose = verbose
        self.debugging = debugging
        self.name = name or "unnamed"

        self.reset()


    def reset(self):
        """Reset the program to the beginning, clearing queues."""

        self.ip = 0
        self.is_running = False
        self.is_waiting = False
        self.inputs = []
        self.outputs = []
        self.step_counter = 0


    def set_program(self, program):
        """Load and initialise a new program."""

        self.program = program.copy()
        self.reset()


    def load_program_from_file(self, filename):
        """Read a single line of comma-separated integers into an array."""

        with open(filename) as f:
            first_line = f.readlines()[0].split(",")

            program = [int(i) for i in first_line]

        self.set_program(program)


    def run(self):
        """Run the program until it exits."""

        if self.is_running:
            raise IntcodeError("Program is already running")

        self.is_running = True

        while self.is_running:
            self.step()


    def has_input(self):
        """Determine whether there's an input value waiting to be read."""

        return len(self.inputs) > 0


    def has_output(self):
        """Determine whether there's an output value waiting to be read."""

        return len(self.outputs) > 0


    def add_input(self, value):
        """Add a new input value to the queue."""

        self.inputs.append(value)


    def add_output(self, value):
        """Add a new output value to the queue."""

        self.outputs.append(value)


    def set_inputs(self, inputs):
        """Populate or overwrite the input queue."""

        self.inputs = inputs


    def get_input(self):
        """Get the first waiting input value and remove it from the queue."""

        if len(self.inputs) == 0:
            raise IntcodeInputError("No input available")

        value = self.inputs[0]
        self.inputs = self.inputs[1:]

        return value


    def get_outputs(self):
        """Get the entire output queue."""

        return self.outputs


    def get_output(self):
        """Get the first waiting output value and remove it from the queue."""

        if len(self.outputs) == 0:
            raise IntcodeError("No output is available")

        value = self.outputs[0]
        self.outputs = self.outputs[1:]

        return value


    def get_opcode(self):
        """Get the current opcode, without parameter mode information."""

        return self.program[self.ip] % 100


    def get_parameter_modes(self):
        """
        Unpack parameter modes from a single integer.

        True: Immediate
        False: Positional
        """

        opcode = int(self.program[self.ip] / 100)
        modes = []

        for i in range(3):
            modes.append(True if opcode % 10 else False)
            opcode = int(opcode / 10)

        return modes


    def get_parameters(self, count):
        """
        Get the parameters for the current opcode, respecting parameter
        modes.
        """

        parameters = []
        modes = self.get_parameter_modes()
        address = self.ip + 1

        for i in range(count):
            value = self.program[address]

            if not modes[i]:
                value = self.program[value]

            parameters.append(value)
            address = address + 1

        return parameters


    def set_memory_value(self, address, value):
        """Poke a value into a memory address."""
        self.program[address] = value


    def jump(self, address):
        """Move the instruction pointer to the specified address."""

        self.ip = address


    def jump_rel(self, delta):
        """Move the instruction pointer by the specified delta."""

        self.ip = self.ip + delta


    def halt(self):
        """Halt execution."""

        if not self.is_running:
            raise IntcodeError("Program is not running")

        self.is_running = False


    def step(self):
        """Run the next single instruction."""

        if not self.is_running:
            raise IntcodeError("Program has halted")

        instruction_set = {
            1: self.add,
            2: self.multiply,
            3: self.input,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.set_if_less_than,
            8: self.set_if_equal,
            99: self.halt
        }

        opcode = self.get_opcode()

        if not opcode in instruction_set:
            raise IntcodeError("Unknown opcode: {opcode}".format(opcode=opcode))

        if self.debugging:
            self.debug()

        self.is_waiting = False

        instruction_set[opcode]()
        self.step_counter = self.step_counter + 1


    def debug(self):
        print ("")
        print ("Machine:", self.name)
        print ("IP:", self.ip)
        print ("Inputs:", self.inputs)
        print ("Outputs:", self.outputs)
        print ("Status:", "running" if self.is_running else "not running", "waiting" if self.is_waiting else "not waiting")

        for x in range(len(self.program)):
            print ("* " if x == self.ip else "  ", x, "] ", self.program[x], sep = "")

        input ("Press enter to continue")


    def add(self):
        """Add."""

        parameters = self.get_parameters(2)
        dest = self.program[self.ip + 3]

        value = parameters[0] + parameters[1]

        if self.verbose:
            print (self.name, self.ip, "(add)", parameters, ":", [dest], "=", value)

        self.set_memory_value(dest, value)
        self.jump_rel(4)


    def multiply(self):
        """Multiply."""

        parameters = self.get_parameters(2)
        dest = self.program[self.ip + 3]

        value = parameters[0] * parameters[1]

        if self.verbose:
            print (self.name, self.ip, "(multiply)", parameters, ":", [dest], "=", value)

        self.set_memory_value(dest, value)
        self.jump_rel(4)


    def input(self):
        """Input."""

        if not self.has_input():
            self.is_waiting = True

            raise IntcodeInputError("No input available")

        dest = self.program[self.ip + 1]

        value = self.get_input()

        if self.verbose:
            print (self.name, self.ip, "(input)", [dest], "=", value)

        self.set_memory_value(dest, value)
        self.jump_rel(2)


    def output(self):
        """Output."""

        parameters = self.get_parameters(1)
        value = parameters[0]

        if self.verbose:
            print (self.name, self.ip, "(output) ", value)

        self.add_output(value)
        self.jump_rel(2)


    def jump_if_true(self):
        """Jump if true."""

        parameters = self.get_parameters(2)
        value = parameters[0]
        dest = parameters[1]

        if self.verbose:
            print (self.name, self.ip, "(jump if true)", parameters)

        if value != 0:
            self.jump(dest)
        else:
            self.jump_rel(3)


    def jump_if_false(self):
        """Jump if false."""

        parameters = self.get_parameters(2)
        value = parameters[0]
        dest = parameters[1]

        if self.verbose:
            print (self.name, self.ip, "(jump if false)", parameters)

        if value == 0:
            self.jump(dest)
        else:
            self.jump_rel(3)


    def set_if_less_than(self):
        """Set if less than."""

        parameters = self.get_parameters(2)
        dest = self.program[self.ip + 3]

        value = 1 if parameters[0] < parameters[1] else 0

        if self.verbose:
            print (self.name, self.ip, "(set if less than) ", parameters, ": ", [dest], "=", value)

        self.set_memory_value(dest, value)
        self.jump_rel(4)


    def set_if_equal(self):
        """Set if equal."""

        parameters = self.get_parameters(2)
        dest = self.program[self.ip + 3]

        value = 1 if parameters[0] == parameters[1] else 0

        if self.verbose:
            print (self.name, self.ip, "(set if equal) ", parameters, ": ", [dest], "=", value)

        self.set_memory_value(dest, value)
        self.jump_rel(4)


    def halt(self):
        if self.verbose:
            print (self.name, self.ip, "(halt)")

        self.is_running = False


class AmplifierGroup:
    """A group of amplifiers connected in series."""

    def __init__(self, sequence, program = None, verbose = False, debugging = False):
        self.amplifiers = []
        self.current_index = 0
        self.carry = None
        self.sequence = sequence
        self.verbose = verbose
        self.debugging = debugging
        self.final_result = None

        names = "ABCDE"

        for phase in sequence:
            amplifier = IntcodeMachine(verbose = verbose, debugging = debugging)

            amplifier.name = names[0]
            names = names[1:]

            if program:
                amplifier.set_program(program)
            else:
                amplifier.load_program_from_file("aoc-7.1.input")

            amplifier.is_running = True
            amplifier.add_input(phase)
            self.amplifiers.append(amplifier)

        self.amplifiers[0].add_input(0)


    def is_waiting(self):
        """Check whether all amplifiers are stuck waiting for input."""

        amplifier_states = [x.is_waiting for x in self.amplifiers]

        return False not in amplifier_states


    def is_running(self):
        """Check whether any amplifiers are still running."""

        amplifier_states = [x.is_running for x in self.amplifiers]

        return True in amplifier_states


    def step(self):
        """Run a single instruction through whichever amplifier is active."""

        amplifier = self.amplifiers[self.current_index]

        while not amplifier.has_output():
            if amplifier.is_waiting:
                raise IntcodeError("Amplifier hanging waiting on input.")

            amplifier.step()

        output = amplifier.get_output()
        self.final_result = output

        # Switch to next amplifier.
        self.current_index = (self.current_index + 1) % len(self.amplifiers)
        next_amplifier = self.amplifiers[self.current_index]
        next_amplifier.add_input(output)


    def run(self):
        """Run a single permutation through the group of amplifiers."""

        while self.is_running():
            self.step()

        return self.final_result


def testIntcodeMachine():
    """Run sample I/O from AoC questions"""

    tests = [
            {
                "name": "nop",
                "program": [1002, 4, 3, 0, 99],
                "inputs": [],
                "outputs": []
             },
             {
                 "name": "print input",
                 "program": [3, 0, 4, 0, 99],
                 "inputs": [123],
                 "outputs": [123]
             },
             {
                 "name": "is non-zero (position mode)",
                 "program": [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],
                 "inputs": [123],
                 "outputs": [1]
             },
             {
                 "name": "is non-zero (position mode, negated)",
                 "program": [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],
                 "inputs": [0],
                 "outputs": [0]
             },
             {
                 "name": "is non-zero (immediate mode)",
                 "program": [3,3,1105,-1,9,1101,0,0,12,4,12,99,1],
                 "inputs": [123],
                 "outputs": [1]
             },
             {
                 "name": "is non-zero (immediate mode, negated)",
                 "program": [3,3,1105,-1,9,1101,0,0,12,4,12,99,1],
                 "inputs": [0],
                 "outputs": [0]
             },
             {
                 "name": "day 5 larger example (less than 8)",
                 "program": [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
                 "inputs": [4],
                 "outputs": [999]
             },
             {
                 "name": "day 5 larger example (equal 8)",
                 "program": [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
                 "inputs": [8],
                 "outputs": [1000]
             },
             {
                 "name": "day 5 larger example (greater than 8)",
                 "program": [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
                 "inputs": [10],
                 "outputs": [1001]
             }
        ]

    overall_success = True

    for test in tests:
        print ("Testing \"", test["name"], "\", ", test["inputs"], " -> ", test["outputs"], sep="")

        machine = IntcodeMachine(verbose = False, debugging = False)
        machine.set_program(test['program'])
        machine.set_inputs(test['inputs'])

        try:
            machine.run()
        except IntcodeError as error:
            print ("Fail: got IntcodeError", error)
            overall_success = False
            print ("--")
            continue

        result = machine.get_outputs()

        if result == test["outputs"]:
            print ("Pass")
        else:
            print ("Fail: got ", result)
            overall_success = False
            exit()

        print ("--")


    return overall_success


def testAmplifierGroup():
    """Run sample I/O from AoC questions"""

    tests = [
            {
                "program": [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5],
                "sequence": [9, 8, 7, 6, 5],
                "output": 139629729
            },
            {
                "program": [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10],
                "sequence": [9, 7, 8, 5, 6],
                "output": 18216
           }
        ]

    overall_success = True

    for test in tests:
        print ("Testing", test["sequence"], "->", test["output"])

        result = None

        group = AmplifierGroup(program = test['program'], sequence = test['sequence'], verbose = False, debugging = False)

        try:
            result = group.run()
        except IntcodeError as error:
            result = group.final_result
            #print ("Fail: got IntcodeError", error)
            #overall_success = False
            #continue

        if result == test["output"]:
            print ("Pass")
        else:
            print ("Fail: got ", result)
            overall_success = False

    print ("--")

    return overall_success


def main():
    if not testIntcodeMachine():
        print("IntcodeMachine tests failed.")
        exit()

    if not testAmplifierGroup():
        print("AmplifierGroup tests failed.")
        exit()

    print ("Tests passed.")

    sequences = list(permutations(range(5, 10)))
    signals = []

    for sequence in sequences:
        group = AmplifierGroup(sequence, verbose = False, debugging = False)

        try:
            result = group.run()
        except IntcodeError as error:
            result = group.final_result

        signals.append(result)

    print ("Result: ", max(signals))


if __name__ == "__main__":
    main()
