import numpy as np
import visualise_puzzle as vis
from node import Node
import heapq
import heuristics

def is_safe(x, y):
    return 0 <= x < 3 and 0 <= y < 3



def beam_search(initial_state, goal_state, empty_tile_pos, beam_width):
    pq = []
    visited = set()  # Set to track visited states
    initial_cost = heuristics.manhattan_distance(initial_state, goal_state)
    root = Node(None, initial_state, empty_tile_pos, initial_cost, 0)
    
    # Use a min-heap to store the nodes
    heapq.heappush(pq, root)
    visited.add(tuple(initial_state.reshape(-1)))
    
    while pq:
        # Limit the number of nodes to explore based on beam width
        if len(pq) > beam_width:
            frontier = heapq.nsmallest(beam_width, pq)
        
        new_frontier = []
        new_visited = set()
        
        for node in pq:
            if node.cost == 0:
                return Node.reconstruct_path(node)
            
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for move in moves:
                new_pos = (node.empty_tile_pos[0] + move[0], node.empty_tile_pos[1] + move[1])
                if is_safe(new_pos[0], new_pos[1]):
                    child = Node.new_node(node.mat, node.empty_tile_pos, new_pos, node.level + 1, node, goal_state)
                    child_tuple = tuple(child.mat.reshape(-1))
                    if child_tuple not in visited and child_tuple not in new_visited:
                        new_visited.add(child_tuple)
                        heapq.heappush(new_frontier, child)
        
        # Update visited and frontier
        visited.update(new_visited)
        frontier = heapq.nsmallest(beam_width, new_frontier)
    
    return None

if __name__ == "__main__":
    # Initial configuration and goal configuration
    initial_state = np.array([[1, 4, 3], [2, 5, 6], [8, 7, 0]])
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    
    # Solve the puzzle
    beam_width = 3
    solution_path = beam_search(initial_state, goal_state, [2, 2], beam_width)
    
    # Visualize the solution path
    if solution_path:
        vis.visualize_puzzle([np.array(state).reshape(3, 3) for state in solution_path], goal_state)
    else:
        print("No solution found.")