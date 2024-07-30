import numpy as np
import visualise_puzzle as vis
import heapq
import heuristics
from node import Node

def isSafe(x, y):
    return 0 <= x < 3 and 0 <= y < 3

def branch_and_bound(initial_state, goal_state, empty_tile_pos):
    pq = []
    visited = set()
    cost = heuristics.manhattan_distance(initial_state, goal_state)
    root = Node(None, initial_state, empty_tile_pos, cost, 0)
    
    heapq.heappush(pq, root)
    visited.add(tuple(root.mat.reshape(-1)))

    while pq:
        min_node = heapq.heappop(pq)
        if min_node.cost == 0:
            return Node.reconstruct_path(min_node)

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for move in moves:
            new_empty_pos = (min_node.empty_tile_pos[0] + move[0], min_node.empty_tile_pos[1] + move[1])
            if isSafe(new_empty_pos[0], new_empty_pos[1]):
                child = Node.new_node(min_node.mat, 
                                min_node.empty_tile_pos, 
                                new_empty_pos, 
                                min_node.level + 1, 
                                min_node, 
                                goal_state)
                child_state_tuple = tuple(child.mat.reshape(-1))
                if child_state_tuple not in visited:
                    heapq.heappush(pq, child)
                    visited.add(child_state_tuple)
    return None

if __name__ == "__main__":
    initial_state = np.array([[1, 4, 3], [2, 5, 6], [8, 7, 0]])
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    empty_tile_pos = tuple(np.argwhere(initial_state == 0)[0])

    solution_path = branch_and_bound(initial_state, goal_state, empty_tile_pos)

    if solution_path:
        vis.visualize_puzzle(solution_path, goal_state)
    else:
        print("No solution found.")