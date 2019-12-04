#!/usr/bin/env python

def isValidPassword(password):
    found_double = False
    previous_digit = 10

    for i in range(6):
        current_digit = password % 10

        if current_digit > previous_digit:
            return False

        if current_digit == previous_digit:
            found_double = True

        previous_digit = current_digit
        password = int(password / 10)

    return found_double


def getPossiblePasswords(start, end):
    return [x for x in range(start, end + 1) if isValidPassword(x)]


def testPasswordCounter():
    """Run sample I/O from AoC question 4.1"""

    if getPossiblePasswords(111111, 111111) != [111111]:
        return False

    if getPossiblePasswords(223450, 223450) != []:
        return False

    if getPossiblePasswords(123789, 123789) != []:
        return False

    return True


def main():
    if not testPasswordCounter():
        print ("Tests failed")
        exit()

    print ("Result: ", len(getPossiblePasswords(193651, 649729)))


if __name__ == "__main__":
    main()
