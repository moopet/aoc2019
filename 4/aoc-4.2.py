#!/usr/bin/env python

import re

def isValidPassword(password):
    found_double = False
    previous_digit = 10
    password_string = str(password)
    digits = [int(password_string[x]) for x in range(6)]

    for i in range(6):
        current_digit = digits[i]
        previous_digit = digits[i - 1] if i else -1

        if current_digit < previous_digit:
            return False

        if current_digit == previous_digit:
            found_double = True

    return found_double


def isTripleFree(password):
    still_has_double = False
    password = str(password)

    # Remove triples.
    for i in range(10):
        password = re.sub(str(i) + r'{3,}', 'x', password)

    for i in range(10):
        if re.search(str(i) + r'{2}', password):
            still_has_double = True

    return still_has_double


def getPossiblePasswords(start, end):
    part1 = [x for x in range(start, end + 1) if isValidPassword(x)]

    return [x for x in part1 if isTripleFree(x)]


def testPasswordCounter():
    """Run sample I/O from AoC question 4.1"""

    if getPossiblePasswords(112233, 112233) != [112233]:
        print ("Testing 112233... failed.")
        return False

    print ("Testing 112233... ok.")

    if getPossiblePasswords(123444, 123444) != []:
        print ("Testing 123444... failed.")
        return False

    print ("Testing 123444... ok.")

    if getPossiblePasswords(111122, 111122) != [111122]:
        print ("Testing 111122... failed.")
        return False

    print ("Testing 111122... ok.")

    return True


def main():
    if not testPasswordCounter():
        print ("Tests failed")
        exit()

    #print (getPossiblePasswords(193651, 649729))
    print ("Result: ", len(getPossiblePasswords(193651, 649729)))


if __name__ == "__main__":
    main()
