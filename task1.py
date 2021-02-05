# Printing factorials recursively by Norbert Kupeczki


import sys


def factorial(number):
    if number > 1:
        result = number * factorial(number - 1)
        print(result)
        return result
    else:
        print(number)
        return number


if __name__ == '__main__':
    factorial(16)
    sys.exit(0)
