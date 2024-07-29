import sys
import numpy as np
import random
import visualise_puzzle as vis
import copy
import heuristics

def is_safe(x, y):
    return 0 <= x < 3 and 0 <= y < 3

# Function to generate neighbors of the current state
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

def hill_climbing(initial_state, goal_state, max_restarts=10):
    """Hill climbing algorithm with random restarts."""
    for _ in range(max_restarts):
        current_state = initial_state
        empty_tile_pos = tuple(np.argwhere(current_state == 0)[0])
        current_cost = heuristics.manhattan_distance(current_state, goal_state)

        # Path tracking
        path = [current_state]

        while True:
            neighbors = get_neighbors(current_state, empty_tile_pos)
            next_state = None
            next_cost = float('inf')  # Initialize with infinity to ensure any found cost is lower

            for neighbor, new_empty_pos in neighbors:
                cost = heuristics.manhattan_distance(neighbor, goal_state)
                if cost < next_cost:
                    next_state = neighbor
                    next_cost = cost
                    new_empty_tile_pos = new_empty_pos

            # If no better neighbor is found, exit
            if next_cost >= current_cost:
                break

            # Update current state and cost
            current_state = next_state
            current_cost = next_cost
            empty_tile_pos = new_empty_tile_pos
            path.append(tuple(current_state.reshape(3,3)))

            # If the goal state is reached, return the path
            if np.array_equal(current_state, goal_state):
                return path

        # Randomly shuffle the initial state to restart
        initial_state = np.random.permutation(initial_state.flatten()).reshape(3, 3)
    
    return None

if __name__ == "__main__":
    # Initial configuration and goal configuration
    initial_state = np.array([[0, 1, 3], [4, 2, 6], [7, 5, 8]])
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    
    # Solve the puzzle
    solution_state = hill_climbing(initial_state, goal_state)

    # Visualize the solution state
    vis.visualize_puzzle([np.array(state).reshape(3, 3) for state in solution_state], goal_state)

    # Check if the goal is reached
    if np.array_equal(solution_state, goal_state):
        print("Goal state reached!")
    else:
        print("Did not reach the goal state.")