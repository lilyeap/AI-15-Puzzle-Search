from heapq import heapq, heapify, heappush, heappop 
from collections import defaultdict 

class Search:
    # def get_children(self, parent_node):
    #     actions = ["R", "U", "D", "L"]
    #     children = []

    #     # for every action, we check the resulting state (the children)
    #     for action in actions:
    #         new_state = parent_node.state.execute_action(action)
    #         if new_state.tiles != parent_node.state.tiles: # if the action causes the board to look the same
    #             children.append(Node(new_state, parent_node, action))
    #     return children

    # check if the current tiles is correct
    def goal_test(self, cur_tiles):
        return cur_tiles == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]



    def reconstructPath(cameFrom, current):
        total_path = {current}
        while (current in cameFrom.keys):
            current = cameFrom[current]
            total_path.prepend(current)

        return total_path


    def A_Star(start, goal, h):
        # initialize a minheap, only start is known
        open_set = []
        heapq.heappush(open_set, (h(start), start))


        cameFrom = {}

        gScore = defaultdict(lambda: float('inf'))
        gScore[start] = 0

        fScore = defaultdict(lambda: float('inf'))
        fScore[start] = h(start)

        # while open_set:
        #     current_priority, current = heapq.heappop(open_set)

        #     if current == goal:
        #         return reconstructPath(current.parent, current)

        #     for neighbor in neighbors[current]:
        #         tentative_g_score = gScore[current] + d(current, neighbor)

        #         if tentative_g_score < gScore[neighbor]:
        #             came_from[neighbor] = current
        #             gScore[neighbor] = tentative_g_score
        #             fScore[neighbor] = tentative_g_score + h(neighbor)
                    
        #             if neighbor not in [item[1] for item in open_set]:
        #                 heapq.heappush(open_set, (fScore[neighbor], neighbor))

        return None  # failure
    
    def solve(self, input):

        initial_list = input.split(" ")
        path, expanded_nodes, time_taken, memory_consumed = self.A_Star(initial_list)
        print("Moves: " + " ".join(path))
        print("Number of expanded Nodes: " + str(expanded_nodes))
        print("Time Taken: " + str(time_taken))
        print("Max Memory (Bytes): " + str(memory_consumed))
        return "".join(path)

