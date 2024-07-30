import numpy as np
import visualise_puzzle as vis
from node import Node
import heuristics
import copy

def is_safe(x, y):
    return 0 <= x < 3 and 0 <= y < 3

def get_neighbors(state, empty_tile_pos):
    neighbors = []
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for move in moves:
        new_pos = (empty_tile_pos[0] + move[0], empty_tile_pos[1] + move[1])
        if is_safe(new_pos[0], new_pos[1]):
            new_state = copy.deepcopy(state)
            x1, y1 = empty_tile_pos
            x2, y2 = new_pos
            new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
            neighbors.append((new_state, new_pos))

    return neighbors

def get_h_cost(mat, goal):
    return heuristics.manhattan_distance(mat, goal_state)

def ida_star(initial_state, goal_state):
    def search(path, g_cost, threshold):
        node = path[-1] #Get the last item

        #f(x) = g(x) + h(x)
        # If the f-cost exceeds the threshold, return the f-cost
        f_cost = g_cost + get_h_cost(node.mat, goal_state)
        if f_cost > threshold:
            return f_cost
        
        # If the current node is the goal state, return 'found'
        if np.array_equal(node.mat, goal_state):
            return 'found'
        
        min_threshold = float('inf') # Initialize to infinity to find the minimum threshold

        # Explore neighbors of the current node
        for neighbor, new_empty_pos in get_neighbors(node.mat, node.empty_tile_pos):
            neighbor_tuple = tuple(neighbor.reshape(-1))
            if neighbor_tuple not in visited:
                child = Node.new_node(node.mat, 
                                      node.empty_tile_pos, 
                                      new_empty_pos, 
                                      node.level + 1, 
                                      node, 
                                      goal_state)
                visited.add(neighbor_tuple)
                path.append(child)
                result = search(path, g_cost + 1, threshold)

                if result == 'found':
                    return result
                
                if result < min_threshold:
                    min_threshold = result

                # Remove the child from the path if it doesn't lead to a solution
                path.pop() #Backtracking

        return min_threshold

    threshold = get_h_cost(initial_state, goal_state)
    root = Node(None, initial_state, tuple(np.argwhere(initial_state == 0)[0]), 0, 0)
    path = [root]

    while True:
        # Reset the visited set for each new threshold iteration
        visited = set()
        visited.add(tuple(root.mat.reshape(-1)))

        # Start the depth-first search with the current threshold
        result = search(path, 0, threshold)
        if result == 'found':
            return Node.reconstruct_path(path[-1])
        if result == float('inf'):
            return None
        
        # Update the threshold for the next iteration
        threshold = result
        

if __name__ == "__main__":
    initial_state = np.array([[1, 4, 3], [2, 5, 6], [8, 7, 0]])
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    solution_path = ida_star(initial_state, goal_state)

    if solution_path:
        vis.visualize_puzzle([np.array(state).reshape(3, 3) for state in solution_path], goal_state)
    else:
        print("No solution found.")