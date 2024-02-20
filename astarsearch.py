from heapq import heapq, heapify, heappush, heappop 
from collections import defaultdict 
import psutil
import time

class Search:

    # check if the current tiles is correct
    def goal_test(self, cur_tiles):
        return cur_tiles == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]



    def reconstructPath(self, cameFrom, current):
        total_path = {current}
        while (current in cameFrom.keys):
            current = cameFrom[current]
            total_path.prepend(current)

        return total_path


    def A_Star(self, start, goal, h):
        # initialize a minheap, only start is known
        open_set = []
        heapq.heappush(open_set, (h(start), start))


        cameFrom = {}

        gScore = defaultdict(lambda: float('inf'))
        gScore[start] = 0

        fScore = defaultdict(lambda: float('inf'))
        fScore[start] = h(start)

        start_time = time.time()
        reached = set()

        while open_set:
            current_priority, current = heapq.heappop(open_set)
            memory_used = psutil.Process().memory_info().rss / 1024  # Memory usage in KB
            if current == goal:
                end_time = time.time()
                path = self.reconstructPath(current.parent, current)
                return path, len(reached), (end_time - start_time), memory_used
        
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


if __name__ == '__main__':
    agent = Search()
    agent.solve("1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12")