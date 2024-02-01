#CS 411 - Assignment 3 Starter Code
#Breadth First Search on 15 Puzzle
#Sarit Adhikari
#Spring 2024

import random
import math
import time
import psutil
import os
from collections import deque
import sys


# This class defines the state of the problem in terms of board configuration
class Board:
    def __init__(self, tiles):
        self.size = int(math.sqrt(len(tiles)))


    # This function returns the resulting state from taking particular action from current state
    def execute_action(self, action):
        pass



# This class defines the node on the search tree, consisting of state, parent and previous action
class Node:
    def __init__(self, state, parent, action):
        pass

    # Returns string representation of the state
    def __repr__(self):
        return str(self.state.tiles)

    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.state.tiles == other.state.tiles

    def __hash__(self):
        return hash(tuple(self.state.tiles))



class Search:




    # This function returns the list of children obtained after simulating the actions on current node
    def get_children(self, parent_node):
        pass

    # This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
    def find_path(self, node):
        pass


    # This function runs breadth first search from the given root node and returns path, number of nodes expanded and total time taken
    def run_bfs(self, root_node):
        pass

    def goal_test(self, cur_tiles):
        pass

    def solve(self, input):

        initial_list = input.split(" ")
        root = Node(Board(initial_list), None, None)
        path, expanded_nodes, time_taken, memory_consumed = self.run_bfs(root)
        print("Moves: " + " ".join(path))
        print("Number of expanded Nodes: " + str(expanded_nodes))
        print("Time Taken: " + str(time_taken))
        print("Max Memory (Bytes): " + str(memory_consumed))
        return "".join(path)

# Testing the algorithm locally
if __name__ == '__main__':
    agent = Search()
    agent.solve("1 2 3 4 5 6 7 8 9 10 11 0 13 14 15 12")