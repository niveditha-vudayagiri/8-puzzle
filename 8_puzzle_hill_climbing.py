import numpy as np
import visualise_puzzle as vis
import heuristics
from node import Node

def is_safe(x, y):
    return 0 <= x < 3 and 0 <= y < 3

# Function to generate neighbors of the current state
def get_neighbors(node, goal_state):
    neighbors = []
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for move in moves:
        new_pos = (node.empty_tile_pos[0] + move[0], node.empty_tile_pos[1] + move[1])
        if is_safe(new_pos[0], new_pos[1]):
            new_node = Node.new_node(node.mat, node.empty_tile_pos, new_pos, node.level + 1, node, goal_state)
            neighbors.append(new_node)

    return neighbors

def hill_climbing(initial_state, goal_state, max_restarts=10):
    """Hill climbing algorithm with random restarts."""
    initial_empty_pos = tuple(np.argwhere(initial_state == 0)[0])
    initial_cost = heuristics.manhattan_distance(initial_state, goal_state)

    for _ in range(max_restarts):
        current_node = Node(None, initial_state, initial_empty_pos, initial_cost, 0)
        path = [current_node]

        while True:
            neighbors = get_neighbors(current_node, goal_state)
            next_node = min(neighbors, key=lambda x: x.cost, default=None)

            # If no better neighbor is found, exit
            if not next_node or next_node.cost >= current_node.cost:
                break

            current_node = next_node
            path.append(current_node)

            # If the goal state is reached, return the path
            if np.array_equal(current_node.mat, goal_state):
                return Node.reconstruct_path(current_node)

        # Randomly shuffle the initial state to restart
        initial_state = np.random.permutation(initial_state.flatten()).reshape(3, 3)
        initial_empty_pos = tuple(np.argwhere(initial_state == 0)[0])
        initial_cost = heuristics.manhattan_distance(initial_state, goal_state)
    
    return None

if __name__ == "__main__":
    # Initial configuration and goal configuration
    initial_state = np.array([[0, 1, 3], [4, 2, 6], [7, 5, 8]])
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    
    # Solve the puzzle
    solution_path = hill_climbing(initial_state, goal_state)

    # Visualize the solution state
    if solution_path:
        vis.visualize_puzzle([np.array(state).reshape(3, 3) for state in solution_path], goal_state)
        print("Goal state reached!")
    else:
        print("Did not reach the goal state.")