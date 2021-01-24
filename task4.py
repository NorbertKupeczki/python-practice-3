# Hash table by Norbert Kupeczki

import sys
import re

int_format = re.compile("^[\-]?[1-9][0-9]*$")
float_format = re.compile("^[\-]?[0-9]*\.?[0-9]+$")


class Data:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.key

    def search(self, key):
        if self.key == key:
            print(f'Key "{self.key}" found, value: {self.value}')
            return True
        elif self.next is not None:
            return self.next.search(key)
        else:
            print("Key not found")
            return False

    def add(self, key, value):
        if self.next is None:
            self.next = Data(key, value)
        else:
            self.next.add(key, value)

    def delete(self, key):
        if self.next.key == key:
            self.next = self.next.next

    def print(self):
        print(f" ->", self.key, end='')
        if self.next is not None:
            self.next.print()
        else:
            print("")


def hash_function(to_hash, table_size):
    if isinstance(to_hash, int):
        h = to_hash % table_size
        print("Key is integer, hash: ", h)
    elif isinstance(to_hash, float):
        h = round(to_hash * table_size % table_size)
        print("Key is float, hash: ", h)
    elif isinstance(to_hash, str):
        h = 0
        for i in to_hash:
            h = h + ord(i)
        h %= table_size
        print("Key is string, hash: ", h)

    return h


def type_finder(inpt):
    if re.match(int_format, inpt):
        return int(inpt)
    elif re.match(float_format, inpt):
        return float(inpt)
    else:
        return str(inpt)


def print_table(table):
    counter = 0
    for i in table:
        if i is None:
            print(f"{counter} : -")
            counter += 1
        else:
            print(counter, ":", end='')
            table[counter].print()
            counter += 1


if __name__ == '__main__':
    hash_table_size = 11
    hash_table = [None] * hash_table_size
    while True:
        key = type_finder(input("\nEnter key: "))
        if key == 'Q':
            break
        h = hash_function(key, hash_table_size)

        if hash_table[h] is None:
            value = input("New key, please enter value: ")
            if hash_table[h] is None:
                hash_table[h] = Data(key, value)

        elif hash_table[h].search(key):
            choice = input("[D]elete, or [N]ew search?")
            if choice.upper() == 'D':
                if hash_table[h].next is None:
                    hash_table[h] = None
                elif hash_table[h].key == key:
                    hash_table[h] = hash_table[h].next
                else:
                    hash_table[h].delete(key)
            else:
                print_table(hash_table)
                continue

        else:
            value = input("New key, please enter value: ")
            hash_table[h].add(key, value)

        print_table(hash_table)

    sys.exit(0)
