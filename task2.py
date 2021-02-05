# Binary search tree by Norbert Kupeczki

import sys
import random


class BinarySearchTree:
    def __init__(self, value): # Constructor initialises this as a node contain some data
        self.left = None
        self.right = None
        self.value = value

    def add(self, node): # Recursively add a node into the correct place in the tree
        if node.value < self.value: # Choose which branch of the search tree
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
        print(self.value, " ", end='')
        if self.right is not None:
            self.right.print()


if __name__ == "__main__":
    values = [random.randint(1, 100) for i in range(20)]
    tree = BinarySearchTree(values[0])
    for value in values[1:]:
        node = BinarySearchTree(value)
        tree.add(node)
    print("\nThe values stored in the Binary Search Tree in ascending order: ")
    tree.print()
    sys.exit(0)
