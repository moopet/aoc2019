#!/usr/bin/env python

import sys
import ipdb
from itertools import permutations
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=1)

class SpaceImageError(Exception):
    pass


class SpaceImage:
    """Representation of a Space Image Format image."""

    def __init__(self):
        self.data = None


    def read_from_file(self, filename):
        """ Read a single line of digits into a string."""

        with open(filename) as f:
            self.data = f.readlines()[0].strip()

    def set_layer_size(self, width, height):
        self.width = width
        self.height = height

        if len(self.data) % (self.width * self.height):
            raise SpaceImageError("Sizes don't match: {width} * {height} != {length}".format(width = width, height = height, length = len(self.data)))


    def convert_to_layers(self):
        layer_length = self.width * self.height
        number_of_layers = int(len(self.data) / layer_length)

        self.layers = [self.data[i * layer_length: (i + 1) * layer_length] for i in range(number_of_layers)]

        if sum([len(x) for x in self.layers]) != len(self.data):
            raise SpaceImageError("Converted sizes don't match")


    def count_digits_in_layer(self, layer_number, digit):
        return self.layers[layer_number].count(str(digit))


    def find_layer_with_fewest(self, digit):
        """
        Find the index of the layer with the fewest of the specified
        digit.
        """

        totals = [x.count(str(digit)) for x in self.layers]

        return totals.index(min(totals))


def main():
    image = SpaceImage()
    image.read_from_file("aoc-8.1.input")
    image.set_layer_size(25, 6)
    image.convert_to_layers()

    layer_number = image.find_layer_with_fewest(0)

    result = image.count_digits_in_layer(layer_number, 1) * image.count_digits_in_layer(layer_number, 2)

    print ("Result: ", result)


if __name__ == "__main__":
    main()
