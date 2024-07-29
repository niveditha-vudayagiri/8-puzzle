import numpy as np
from collections import deque
import visualise_puzzle as vis

def neighbors(state):
    """Generate the neighbors of the current state by moving the empty tile."""
    zero_pos = tuple(np.argwhere(state == 0)[0])
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    neighbors = []
    
    for move in moves:
        new_pos = (zero_pos[0] + move[0], zero_pos[1] + move[1])
        if 0 <= new_pos[0] < 3 and 0 <= new_pos[1] < 3:
            new_state = np.copy(state)
            new_state[zero_pos], new_state[new_pos] = new_state[new_pos], new_state[zero_pos]
            neighbors.append(new_state)
    
    return neighbors

def tuple_from_state(state):
    """Convert a numpy array state to a tuple for hashing."""
    return tuple(state.reshape(-1))

def expand_frontier(frontier, explored, other_explored, side):
    """Expand the search frontier and check for intersection with the other side."""
    curr = frontier.popleft()
    curr_array = np.array(curr).reshape(3, 3)

    for neighbor in neighbors(curr_array):
        neighbor_tuple = tuple_from_state(neighbor)
        if neighbor_tuple in other_explored:
            explored[neighbor_tuple] = curr
            return reconstruct_path(neighbor, explored, other_explored, side)  # If yes, reconstruct path
        
        if neighbor_tuple not in explored:
            frontier.append(neighbor_tuple)
            explored[neighbor_tuple] = curr
    
    return None

def bidirectional_search(start, goal):
    """Bidirectional search for the 8-puzzle."""
    start_tuple = tuple_from_state(start)
    goal_tuple = tuple_from_state(goal)
    
    if start_tuple == goal_tuple:
        return [start_tuple]
    
    # Initialize frontiers
    frontier_start = deque([start_tuple])
    frontier_goal = deque([goal_tuple])
    
    # Initialize explored sets
    explored_start = {start_tuple: None}
    explored_goal = {goal_tuple: None}
    
    while frontier_start and frontier_goal:
        # Expand the search from the start side
        path_found = expand_frontier(frontier_start, explored_start, explored_goal, 'start')
        if path_found:
            return path_found
        
        # Expand the search from the goal side
        path_found = expand_frontier(frontier_goal, explored_goal, explored_start, 'goal')
        if path_found:
            return path_found
    
    return None  # No path found

def reconstruct_path(meeting_point, parent_start, parent_goal, meeting_side):
    """Reconstruct the path from start to goal through the meeting point."""
    path = []
    
    # Convert meeting point back to numpy array
    meeting_point_array = np.array(meeting_point).reshape(3, 3)
    
    if meeting_side == 'start':
        path.extend(trace_path(meeting_point_array, parent_start, reverse=True))
        path.extend(trace_path(meeting_point_array, parent_goal, reverse=False)[1:])
    else:  # meeting_side == 'goal'
        path.extend(trace_path(meeting_point_array, parent_goal, reverse=False))
        path.extend(trace_path(meeting_point_array, parent_start, reverse=True)[1:])
    
    return path

def trace_path(start, parent_map, reverse):
    """Trace a path from a node to the root, optionally reversing it."""
    path = []
    node = tuple_from_state(start)
    
    while node:
        path.append(node)
        node = parent_map.get(node)  # Use tuple_from_state to get correct parent
    
    if reverse:
        path.reverse()
    
    return path

if __name__ == "__main__":
    # Initial configuration and goal configuration
    initial_state = np.array([[1, 4, 3], [2, 5, 6], [8, 7, 0]])
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    
    # Solve the puzzle
    solution_path = bidirectional_search(initial_state, goal_state)

    # Visualize the solution path
    if solution_path:
        vis.visualize_puzzle([np.array(state).reshape(3, 3) for state in solution_path], goal_state)
    else:
        print("No solution found.")