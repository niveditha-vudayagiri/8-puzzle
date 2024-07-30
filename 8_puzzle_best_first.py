import numpy as np
import heapq
import visualise_puzzle as vis
import heuristics
from node import Node

def is_safe(x, y):
    return 0 <= x < 3 and 0 <= y < 3

def best_first_search(initial_state, goal_state, empty_tile_pos):
    pq = []
    visited = set()
    initial_cost = heuristics.manhattan_distance(initial_state, goal_state)
    root = Node(None, initial_state, empty_tile_pos, initial_cost, 0)
    
    heapq.heappush(pq, root)
    visited.add(tuple(initial_state.reshape(-1)))
    
    while pq:
        current_node = heapq.heappop(pq)
        
        if np.array_equal(current_node.mat, goal_state):
            return Node.reconstruct_path(current_node)
        
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for move in moves:
            new_pos = (current_node.empty_tile_pos[0] + move[0], current_node.empty_tile_pos[1] + move[1])
            if is_safe(new_pos[0], new_pos[1]):
                child = Node.new_node(current_node.mat, current_node.empty_tile_pos, new_pos, current_node.level + 1, current_node, goal_state)
                child_tuple = tuple(child.mat.reshape(-1))
                if child_tuple not in visited:
                    visited.add(child_tuple)
                    heapq.heappush(pq, child)
    
    return None

if __name__ == "__main__":
    initial_state = np.array([[1, 4, 3], [2, 5, 6], [8, 7, 0]])
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    
    solution_path = best_first_search(initial_state, goal_state, [2, 2])
    
    if solution_path:
        vis.visualize_puzzle([np.array(state).reshape(3, 3) for state in solution_path], goal_state)
    else:
        print("No solution found.")