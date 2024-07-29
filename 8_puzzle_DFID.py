import numpy as np
import visualise_puzzle as vis

def dfs_limited(current_state, goal_state, depth_limit, path, visited):
    """Performs Depth-Limited Search (DLS) up to a given depth limit."""
    if np.array_equal(current_state, goal_state):
        return path
    if depth_limit == 0:
        return None

    zero_pos = tuple(np.argwhere(current_state == 0)[0])
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    for move in moves:
        new_pos = (zero_pos[0] + move[0], zero_pos[1] + move[1])
        if 0 <= new_pos[0] < 3 and 0 <= new_pos[1] < 3:
            new_state = np.copy(current_state)
            new_state[zero_pos], new_state[new_pos] = new_state[new_pos], new_state[zero_pos]
            new_state_tuple = tuple(new_state.reshape(-1))
            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                result_path = dfs_limited(new_state, goal_state, depth_limit - 1, path + [new_state], visited)
                if result_path:
                    return result_path
                visited.remove(new_state_tuple)  # Backtrack

    return None

def dfid_solve(initial_state, goal_state):
    """Solves the 8-puzzle using Depth-First Iterative Deepening (DFID)."""
    depth_limit = 0
    while True:
        visited = set()
        visited.add(tuple(initial_state.reshape(-1)))
        result_path = dfs_limited(initial_state, goal_state, depth_limit, [initial_state], visited)
        if result_path is not None:
            return result_path
        depth_limit +=1

if __name__ == "__main__":
    # Initial configuration and goal configuration
    initial_state = np.array([[1, 4, 3], [2, 5, 6], [8, 7, 0]])
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    # Solve the puzzle
    solution_path = dfid_solve(initial_state, goal_state)

    # Visualize the solution path
    if solution_path:
        vis.visualize_puzzle(solution_path, goal_state)
    else:
        print("No solution found.")