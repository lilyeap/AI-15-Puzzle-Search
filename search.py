import time
import sys

goal_state = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

class Search:

    def goal_test(self, cur_tiles):
        return cur_tiles == goal_state

    def get_neighbors(self, tiles):
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]  
        neighbors = []
        empty_idx = tiles.index('0')
        empty_row, empty_col = empty_idx // 4, empty_idx % 4

        for dr, dc in moves:
            new_row, new_col = empty_row + dr, empty_col + dc
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                new_tiles = tiles[:]
                swap_idx = new_row * 4 + new_col
                new_tiles[empty_idx], new_tiles[swap_idx] = new_tiles[swap_idx], new_tiles[empty_idx]
                neighbors.append(new_tiles)
        return neighbors

    def manhattan_distance(self, state):
        distance = 0
        for i, tile in enumerate(state):
            if tile != '0':
                goal_idx = goal_state.index(tile)
                distance += abs(i // 4 - goal_idx // 4) + abs(i % 4 - goal_idx % 4)
        return distance
    
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

    def IDA_star(self, initial_state):
        threshold = self.manhattan_distance(initial_state)
        while True:
            response = self.search(initial_state, 0, threshold, [])
            if response[0]:  # Found solution
                return response[1], response[2]  # Moves, Number of Nodes Expanded
            elif response[1] == float('inf'):  # No solution
                return None, response[2]
            else:
                threshold = response[1]  # New threshold

    def search(self, current_state, g, threshold, path):
        f = g + self.manhattan_distance(current_state)
        if f > threshold:
            return False, f, 0  # False, New Threshold, Nodes Expanded
        if self.goal_test(current_state):
            return True, path, 1  # Found, Path, Nodes Expanded
        min_threshold = float('inf')
        nodes_expanded = 1
        for neighbor in self.get_neighbors(current_state):
            move = self.get_move(current_state, neighbor)
            found, new_path, expanded = self.search(neighbor, g + 1, threshold, path + [move])
            nodes_expanded += expanded
            if found:
                return True, new_path, nodes_expanded
            if new_path < min_threshold:
                min_threshold = new_path
        return False, min_threshold, nodes_expanded

    def solve(self, input):
        initial_list = input.split(" ")
        moves, expanded_nodes = self.IDA_star(initial_list)
        if moves:
            print("Moves: " + " ".join(moves))
        else:
            print("Solution not found.")
        print("Number of expanded Nodes: " + str(expanded_nodes))

if __name__ == '__main__':
    agent = Search()
    agent.solve("1 0 3 4 5 2 6 8 9 10 7 11 13 14 15 12")
