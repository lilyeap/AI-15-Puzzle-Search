import random
import math
import time
import psutil
import os
from collections import deque
import sys
from heapq import *


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


#This class defines the node on the search tree, consisting of state, parent and previous action		
class Node:
	def __init__(self,state,parent,action):
		self.state = state
		self.parent = parent
		self.action = action
		if parent is None:
			self.cost=0
		else:
			self.cost = parent.cost+1
	
	#Returns string representation of the state	
	def __repr__(self):
		return str("state: " +str(self.state.tiles) + "prev_action "+ str(self.action))
	
	#Comparing current node with other node. They are equal if states are equal	
	def __eq__(self,other):
		return self.state.tiles == other.state.tiles
		
	def __lt__(self, other):
		return id(self)<= id(other)
	
	def __hash__(self):
		return hash(tuple(self.state.tiles))


#This class defines astar search problem        
class Astar:
    def __init__(self,start,goal,heuristic):
        self.root_node = start
        self.goal_state = goal
        self.heuristic = heuristic
        self.node_expanded = 0
        
    def run(self):
        threshold = self.h_value(self.root_node)
        while True:
            response = self.search(self.root_node, threshold)
            if type(response) is list:  # Solution found
                return response
            threshold = response  # Update the threshold for the next iteration

    def search(self, node, threshold):
        f_value = node.cost + self.h_value(node)
        if f_value > threshold:
            return f_value  # This f_value becomes the new threshold if no solution is found

        if self.goal_test(node.state.tiles):
            return self.find_path(node)  # Solution found

        min_threshold = float('inf')
        for child in self.get_children(node):
            temp = self.search(child, threshold)
            if type(temp) is list:  # Solution found
                return temp
            if temp < min_threshold:
                min_threshold = temp
        return min_threshold
    
    def f_value(self,node):
        return node.cost + self.h_value(node)
        
    def h_value(self,node):
        if self.heuristic=="manhattan":
            return self.manhattan_heuristic(node)
        else:
            return self.misplaced_tiles_heuristic(node)
    
    #This function calculates sum of manhattan distances of each tile from goal position
    def manhattan_heuristic(self,node):
        tiles = node.state.tiles
        size = node.state.size
        total_sum_distances = 0 
        for i in range(0,len(tiles)):
            value = int(tiles[i])
            if value==0 : continue
            current_x = i / size
            current_y = i % size
            correct_x = (value-1) / size
            correct_y = (value-1) % size
            
            
            cur_distance = abs(correct_x-current_x) + abs(correct_y-current_y)
            total_sum_distances += cur_distance
        return total_sum_distances
    
    #This function calculates number of misplaced tiles from goal position
    def misplaced_tiles_heuristic(self,node):
        tiles = node.state.tiles
        num_misplaced = 0
        for i in range(1,len(tiles)):
            if i!=int(tiles[i-1]) : num_misplaced+=1
            
        return num_misplaced
        
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
        
    #Utility function checking if current state is goal state or not
    def goal_test(self,cur_state):
        return cur_state == self.goal_state


class Search:

    # Utility function to randomly generate 15-puzzle
    def generate_puzzle(self, size):
        numbers = list(range(size * size))
        random.shuffle(numbers)
        return Node(Board(numbers), None, None)


    def solve(self, input):
        initial_time = time.time()
        initial_list = input.split(" ")
        root = Node(Board(initial_list), None, None)
        
        goal_state = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0']    
    
        #astar with manhattan distance heurisitcs
        astar = Astar(root, goal_state,"manhattan")
        # print("manhattan_heuristic: "+ str(astar.manhattan_heuristic(root)))
        
        #astar with misplaced tiles heurisitcs
        # astar = Astar(root, goal_state,"misplaced")
        # print("misplaced tiles heuristic: "+ str(astar.misplaced_tiles_heuristic(root)))
        
        solution = astar.run()
        final_time = time.time()
        
        print("Moves: "+ str(solution[0]))
        print("Number of expanded Nodes:" + str(solution[1]))
        print("Time Taken: "+str(final_time-initial_time))
        print("Max Memory: "+str(solution[2])+" KB")
        

        return "".join(solution[0])

if __name__ == '__main__':
    agent = Search()
    agent.solve("5 1 2 3 9 6 7 4 13 10 11 8 0 14 15 12")