#CS 411 - Assignment 3
#Breadth First Search on 15 Puzzle
#Lily Eap
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
   # initialize the board
    def __init__(self, tiles):
        # convert the string array of numbers into an int array called tiles
        self.tiles = []
        for tile in tiles:
            self.tiles.append(int(tile))

    # This function returns the resulting state from taking particular action from current state
    def execute_action(self, action):
        # create a copy of the existing tiles
        mod_tiles = self.tiles[:]

        # find index where the empty tile is
        blank_tile = mod_tiles.index(0)

        # action is to move up and the empty square is NOT in the top row
        if action == "U" and blank_tile > 3:
            # switch the empty tile with above tile
            temp = mod_tiles[blank_tile]
            mod_tiles[blank_tile] = mod_tiles[blank_tile - 4]
            mod_tiles[blank_tile - 4] = temp
        
        # action is to move down and the empty square is NOT in the bottom row
        elif action == "D" and blank_tile < 12:
            # switch the empty tile with below tile
            temp = mod_tiles[blank_tile]
            mod_tiles[blank_tile] = mod_tiles[blank_tile + 4]
            mod_tiles[blank_tile + 4] = temp
        
        # action is to move left and the empty square is NOT in the left column
        elif action == "L" and blank_tile % 4 != 0:
            # switch the empty tile with right tile
            temp = mod_tiles[blank_tile]
            mod_tiles[blank_tile] = mod_tiles[blank_tile - 1]
            mod_tiles[blank_tile - 1] = temp

        # action is to move right and the empty square is NOT in the right column
        elif action == "R" and blank_tile % 4 != 3:
            # switch the empty tile with left tile
            temp = mod_tiles[blank_tile]
            mod_tiles[blank_tile] = mod_tiles[blank_tile + 1]
            mod_tiles[blank_tile + 1] = temp

        return Board(mod_tiles)



# This class defines the node on the search tree, consisting of state, parent and previous action
class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

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
        actions = ["R", "U", "D", "L"]
        children = []

        # for every action, we check the resulting state (the children)
        for action in actions:
            new_state = parent_node.state.execute_action(action)
            if new_state.tiles != parent_node.state.tiles: # if the action causes the board to look the same
                children.append(Node(new_state, parent_node, action))
        return children


    # This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
    def find_path(self, node):
        actions = []

        # traverse to each node's parent and keep track of path w/ list
        while node.parent: 
            actions.append(node.action) 
            node = node.parent 
        
        # we reverse the actions list to get it in the order from parent state to final state
        actions.reverse()
        return actions


    # This function runs breadth first search from the given root node and returns path, number of nodes expanded and total time taken
    def run_bfs(self, root_node):
        # store initial start time
        init_time = time.time()

        # initialized frontier with root node and set to keep track of what states we've explored
        reached = set()
        frontier = deque([root_node])
        expanded_nodes = 0 

        while frontier:
            # remove the node to be explored
            node = frontier.popleft()
            
            # if the current state is the goal state, backtrack to find solution path and finish program
            if self.goal_test(node.state.tiles):
                path = self.find_path(node)
                expanded_nodes += 1

                frontier_mem = sys.getsizeof(frontier)
                reached_mem = sys.getsizeof(reached)
                total_mem = frontier_mem + reached_mem

                return path, expanded_nodes, time.time() - init_time, total_mem

            # for each possible move that would result in a different state
            for child in self.get_children(node):

                # if we have never seen that state before (reached) 
                # and if it's not a state that we already planned to explore (not in frontier)
                if tuple(child.state.tiles) not in reached and child not in frontier:
                    reached.add(tuple(child.state.tiles))
                    frontier.append(child)
                    expanded_nodes += 1


        frontier_mem = sys.getsizeof(frontier)
        reached_mem = sys.getsizeof(reached)
        total_mem = frontier_mem + reached_mem

        # goal state is not found... 
        return [], expanded_nodes, time.time() - init_time, total_mem


    # check if the current tiles is correct
    def goal_test(self, cur_tiles):
        return cur_tiles == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

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
    agent.solve("1 0 3 4 5 2 6 8 9 10 7 11 13 14 15 12")