#CS 411 - Assignment 5
#A Star Search on 15 Puzzle
#Lily Eap
#Spring 2024

import heapq
import psutil
from collections import defaultdict
import time
import sys

goal_state = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

class Search:

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

    # calculate the Manhattan distance heuristic for a given state
    def manhattan_distance(self, state):
        distance = 0
        for i, tile in enumerate(state):
            if tile != '0':
                goal_idx = goal_state.index(tile)
                distance += abs(i // 4 - goal_idx // 4) + abs(i % 4 - goal_idx % 4)
        return distance

    # calculate the misplaced tiles heuristic for a given state
    def misplaced_tiles(self, state):
        return sum(1 for cur, goal in zip(state, goal_state) if cur != goal and cur != '0')
    
    # determine the move made between two states
    def get_move(self, current_state, next_state):
        empty_idx = current_state.index('0')
        next_idx = next_state.index('0')
        if empty_idx - next_idx == 1:
            return 'L'
        elif empty_idx - next_idx == -1:
            return 'R'
        elif empty_idx - next_idx == 4:
            return 'U'
        elif empty_idx - next_idx == -4:
            return 'D'
        else:
            return ''
        
    # this function runs a* search from the given root node and returns path, number of nodes expanded and total time taken
    def A_Star(self, initial_state, heuristic="manhattan"):
        pq = []
        heapq.heappush(pq, (0, initial_state, ""))  # (priority, state, path)

        explored = set()
        start_time = time.time()
        total_mem = 0

        while pq:
            _, current_state, path = heapq.heappop(pq)
            state_str = "".join(current_state)

            # calculate total memory
            frontier_mem = sys.getsizeof(pq)
            reached_mem = sys.getsizeof(explored)
            found_mem = frontier_mem + reached_mem
            total_mem = max(total_mem, found_mem)

            # if the current state is the goal state, backtrack to find solution path and finish program
            if self.goal_test(current_state):
                end_time = time.time()
                return path, len(explored), (end_time - start_time), total_mem
        
            explored.add(state_str)

            # explore each neighbor
            for neighbor in self.get_neighbors(current_state):
                neighbor_str = "".join(neighbor)

                if neighbor_str not in explored:
                    # calculate priority based on the chosen heuristic
                    if heuristic == "manhattan":
                        priority = len(path) + self.manhattan_distance(neighbor)
                    elif heuristic == "misplaced":
                        priority = len(path) + self.misplaced_tiles(neighbor)
                    else:
                        priority = len(path) + self.manhattan_distance(neighbor)

                    heapq.heappush(pq, (priority, neighbor, path + self.get_move(current_state, neighbor)))
    
    def solve(self, input):

        initial_list = input.split(" ")
        path, expanded_nodes, time_taken, memory_consumed = self.A_Star(initial_list, heuristic="misplaced")
        print("Moves: " + " ".join(path))
        print("Number of expanded Nodes: " + str(expanded_nodes))
        print("Time Taken: " + str(time_taken))
        print("Max Memory (Bytes): " + str(memory_consumed))
        return "".join(path)


if __name__ == '__main__':
    agent = Search()
    agent.solve("1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12")