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
        self.size = int(math.sqrt(len(tiles)))  # defining length/width of the board
        self.tiles = tiles

    # This function returns the resulting state from taking particular action from current state
    def execute_action(self, action):
        new_tiles = self.tiles[:]
        empty_index = new_tiles.index('0')
        if action == 'L':
            if empty_index % self.size > 0:
                new_tiles[empty_index - 1], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[empty_index - 1]
        if action == 'R':
            if empty_index % self.size < (self.size - 1):
                new_tiles[empty_index + 1], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[empty_index + 1]
        if action == 'U':
            if empty_index - self.size >= 0:
                new_tiles[empty_index - self.size], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[
                    empty_index - self.size]
        if action == 'D':
            if empty_index + self.size < self.size * self.size:
                new_tiles[empty_index + self.size], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[
                    empty_index + self.size]
        return Board(new_tiles)


# This class defines the node on the search tree, consisting of state, parent and previous action
class Node:
    def __init__(self, state, parent, action, depth = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth

    # Returns string representation of the state
    def __repr__(self):
        return str(self.state.tiles)

    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.state.tiles == other.state.tiles

    def __hash__(self):
        return hash(tuple(self.state.tiles))



class Search:

    # Utility function to randomly generate 15-puzzle
    def generate_puzzle(self, size):
        numbers = list(range(size * size))
        random.shuffle(numbers)
        return Node(Board(numbers), None, None)

    # This function returns the list of children obtained after simulating the actions on current node
    def get_children(self, parent_node):
        children = []
        actions = ['L', 'R', 'U', 'D']  # left,right, up , down ; actions define direction of movement of empty tile
        for action in actions:
            child_state = parent_node.state.execute_action(action)
            child_node = Node(child_state, parent_node, action)
            children.append(child_node)
        return children

    # This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
    def find_path(self, node):
        path = []
        while (node.parent is not None):
            path.append(node.action)
            node = node.parent
        path.reverse()
        return path

    def is_cycle(self, node):
        seen = set()

        while node is not None:
            if node in seen:
                return True  
            seen.add(node)
            node = node.parent
        return False
    

    # # This function runs iddfs from the given root node and returns path, number of nodes expanded and total time taken

    def dls(self, problem, limit, reached):
        frontier = [problem]
        result = "failure"
        while frontier:
            
            node = frontier.pop()
            if node in reached:
                continue
            
            reached.add(node)

            memory = sys.getsizeof(frontier) + sys.getsizeof(reached)
            if self.goal_test(node.state.tiles):
                return node, "win", memory
            if node.depth > limit:
                result = "cutoff"
            else:
                print(self.get_children(node))
                for child in self.get_children(node):
                    if self.is_cycle(child):
                        print("cycle")
                    if child not in reached and not self.is_cycle(child): 
                        frontier.append(Node(child.state, node, child.action, node.depth + 1))
                    
        
        return None, result, sys.getsizeof(frontier) + sys.getsizeof(reached)





    # This function runs IDDFS from the given root node and returns path, number of nodes expanded and total time taken
    def run_bfs(self, root_node):
        depth = 0

        start_time = time.time()
        reached = set()
        max_memory = 0
        while True:
            
            result, status, found_mem = self.dls(root_node, depth, reached)
            max_memory = max(max_memory, found_mem)

            if status == "win":
                end_time = time.time()
                path = self.find_path(result)
                return path, len(reached), (end_time - start_time), max_memory
            elif status == "loss":
                end_time = time.time()
                return [], len(reached), (end_time - start_time), max_memory
            
            depth += 1
            reached= set()


    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

    def solve(self, input):

        initial_list = input.split(" ")
        root = Node(Board(initial_list), None, None)
        path, expanded_nodes, time_taken, memory_consumed = self.run_bfs(root)
        print("Moves: " + " ".join(path))
        print("Number of expanded Nodes: " + str(expanded_nodes))
        print("Time Taken: " + str(time_taken))
        print("Max Memory (Bytes): " + str(memory_consumed))
        return "".join(path)

if __name__ == '__main__':
    agent = Search()
    agent.solve("1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12")