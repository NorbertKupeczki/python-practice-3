# Guess the number game using binary search tree by Norbert Kupeczki

import sys
import random


class BinarySearchTree:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

    def add(self, node):
        if node.value < self.value:
            if self.left is not None:
                self.left.add(node)
            else:
                self.left = node
        else:
            if self.right is not None:
                self.right.add(node)
            else:
                self.right = node

    def print(self):
        if self.left is not None:
            self.left.print()
        print(self.value)
        if self.right is not None:
            self.right.print()

    def search(self, number):
        if self.value == int(number):
            print("Value found: ", + self.value)
            game.guess = True
            return True
        elif self.value > int(number) and self.left is not None:
            self.left.search(number)
        elif self.value < int(number) and self.right is not None:
            self.right.search(number)
        else:
            print(f"Value is not in the tree.")
            tree.closest_number(number)
            return False

    def search_smallest(self):
        if self.left is not None:
            self.left.search_smallest()
        else:
            print("Smallest value in the range: ", + self.value)

    def search_highest(self):
        if self.right is not None:
            self.right.search_highest()
        else:
            print("Highest value in the range: ", + self.value)

    def closest_number(self, number, distance=100):
        if distance > abs(self.value - int(number)):
            distance = abs(self.value - int(number))
        if self.value > int(number) and self.left is not None:
            self.left.closest_number(number, distance)
        elif self.value < int(number) and self.right is not None:
            self.right.closest_number(number, distance)
        else:
            print(f"The closest number is {distance} away")


class Game:
    is_running = True
    guess = False

    @staticmethod
    def game_instructions():
        print("*" * 89)
        print("""Welcome to the number guess game. The goal is to successfully guess one of the 20 numbers
within a certain range. If you fail to guess correctly, a hint will be given.""")
        print("*" * 89, "\n")


if __name__ == "__main__":
    game = Game
    values = [random.randint(1, 100) for i in range(20)]
    tree = BinarySearchTree(values[0])
    for value in values[1:]:
        node = BinarySearchTree(value)
        tree.add(node)
    # tree.print()
    game.game_instructions()
    tree.search_smallest()
    tree.search_highest()
    while game.is_running:
        to_search = input("Enter your guess: ")
        tree.search(to_search)
        if game.guess:
            print("\nCongratulations, you guessed the number!")
            game.is_running = False
        else:
            print("Try again!\n")
    sys.exit(0)
