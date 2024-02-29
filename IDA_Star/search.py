#CS 411 - Assignment 6
#IDA Star Search on 15 Puzzle
#Lily Eap
#Spring 2024

import time
import sys

goal_state = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

class Search:
    def __init__(self):
        self.visited = set() # track visited states

    # check if the current tiles is correct
    def goal_test(self, cur_tiles):
        return cur_tiles == goal_state

    # getting all possible states that can be reached after making a single move
    def get_neighbors(self, tiles):
        # define the possible moves (UP, DOWN, LEFT, RIGHT)
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]  
        neighbors = []

        # find the position of the empty space ('0')
        empty_idx = tiles.index('0')
        empty_row, empty_col = empty_idx // 4, empty_idx % 4

        # generate neighbors by swapping the empty tile with adjacent tiles
        for dr, dc in moves:
            new_row, new_col = empty_row + dr, empty_col + dc
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                new_tiles = tiles[:]
                swap_idx = new_row * 4 + new_col

                # make sure to swap using consistent data types if needed
                new_tiles[empty_idx], new_tiles[swap_idx] = new_tiles[swap_idx], new_tiles[empty_idx]
                neighbors.append(new_tiles)
        return neighbors


    # calculate the misplaced tiles heuristic for a given state
    def misplaced_tiles(self, state):
        return sum(1 for cur, goal in zip(state, goal_state) if cur != goal and cur != '0')
    
    # calculate the Manhattan distance heuristic for a given state
    def manhattan_distance(self, state):
        distance = 0
        for i, tile in enumerate(state):
            if tile != '0':
                goal_idx = goal_state.index(tile)
                distance += abs(i // 4 - goal_idx // 4) + abs(i % 4 - goal_idx % 4)
        return distance
    
    # determine the move made between two states
    def get_move(self, current_state, next_state):
        diff = current_state.index('0') - next_state.index('0')
        if diff == 1:
            return 'L'
        elif diff == -1:
            return 'R'
        elif diff == 4:
            return 'U'
        elif diff == -4:
            return 'D'
        return ''

    # this function runs ida* search from the given root node and returns path, number of nodes expanded and total time taken
    def IDA_star(self, initial_state, heuristic="manhattan"):
        # initialize threshold based on the selected heuristic
        if heuristic == "manhattan":
            threshold = self.manhattan_distance(initial_state)
        elif heuristic == "misplaced":
            threshold = self.misplaced_tiles(initial_state)

        self.visited = set() 
        start_time = time.time()

         # iterative deepening depth-first search until solution is found unless unsolvable
        while True:
            self.visited.clear()  
            
            found, new_path, expanded_nodes, memory_consumed, new_threshold = self.search(initial_state, 0, threshold, [], heuristic)

            end_time = time.time()

            if found: # return the solution path and stats if found
                return new_path, expanded_nodes, (end_time - start_time), memory_consumed
            elif new_threshold == float('inf'):   # no solution found
                return None, expanded_nodes, (end_time - start_time), memory_consumed
            else: # update the threshold if we continue searching
                threshold = new_threshold  

    # recursive depth-first search with iterative deepening and 
    # returns if goal state is found, path, num of nodes expanded on that threshold, max mem, and new threshold value for next iteration
    def search(self, current_state, g, threshold, path, heuristic="manhattan"):
        self.visited.add(tuple(current_state))  # mark the state as visited

        # initialize f score based on the selected heuristic and g score
        if heuristic == "manhattan":
            f = g + self.manhattan_distance(current_state)
        elif heuristic == "misplaced":
            f = g + self.misplaced_tiles(current_state)

        # check if f is bigger than threshold, and if so, prune
        if f > threshold:
            return False, float('inf'), 0, 0, f  

        # check if current state is the goal
        if self.goal_test(current_state):
            return True, path, 1, sys.getsizeof(path), threshold  

        min_threshold = float('inf')
        nodes_expanded = 1
        total_mem = sys.getsizeof(path)

        # explore each neighbor
        for neighbor in self.get_neighbors(current_state):
            if tuple(neighbor) not in self.visited:
                move = self.get_move(current_state, neighbor)
                found, new_path, expanded, mem_used, temp_threshold = self.search(neighbor, g + 1, threshold, path + [move], heuristic)
                nodes_expanded += expanded
                total_mem = max(total_mem, mem_used)

                if found:
                    return True, new_path, nodes_expanded, total_mem, threshold 

                # update min_threshold if temp_threshold is the smallest value exceeding current threshold
                if temp_threshold < min_threshold and temp_threshold > threshold:
                    min_threshold = temp_threshold
        self.visited.remove(tuple(current_state))

        return False, path, nodes_expanded, total_mem, min_threshold

    def solve(self, input):
        initial_list = input.split(" ")
        path, expanded_nodes, time_taken, memory_consumed = self.IDA_star(initial_list, heuristic="manhattan")
        if path:
            print("Moves: " + " ".join(path))
        else:
            print("Solution not found.")
        print("Number of expanded Nodes: " + str(expanded_nodes))
        print("Time Taken: " + str(time_taken))
        print("Max Memory (Bytes): " + str(memory_consumed))
        return "".join(path)

if __name__ == '__main__':
    agent = Search()
    agent.solve("5 2 4 8 10 3 11 14 6 0 9 12 13 1 15 7")