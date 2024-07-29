import numpy as np
from queue import Queue
import visualise_puzzle as vis

def bfs_solve(initial_state, goal_state):
    """Solves the 8-puzzle using Breadth-First Search (BFS)."""
    queue = Queue()
    queue.put((initial_state, [initial_state]))
    visited = set()
    visited.add(tuple(initial_state.reshape(-1)))
    
    while not queue.empty():
        current_state, path = queue.get()
        if np.array_equal(current_state, goal_state):
            return path
        
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
                    queue.put((new_state, path + [new_state]))

    return None  

if __name__ == "__main__":
    # Initial configuration and goal configuration
    initial_state = np.array([[1, 4, 3], [2, 5, 6], [8, 7, 0]])
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    # Solve the puzzle
    solution_path = bfs_solve(initial_state, goal_state)

    # Visualize the solution path
    if solution_path:
        vis.visualize_puzzle(solution_path, goal_state)
    else:
        print("No solution found.")