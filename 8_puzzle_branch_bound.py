import numpy as np
import copy
import visualise_puzzle as vis
from priority_queue import priorityQueue
import heuristics

def isSafe(x, y):
    return 0 <= x < 3 and 0 <= y < 3

# Node structure
class Node:
    def __init__(self, parent, mat, empty_tile_pos, cost, level):
        self.parent = parent
        self.mat = mat
        self.empty_tile_pos = empty_tile_pos
        self.cost = cost
        self.level = level

    #C(x) = g(x) + h(x)
    # g(x) -> is the number of moves taken so far. 
    # h(x) -> is the number of tiles not in their goal positions.
    def __lt__(self, nxt):
        return self.cost + self.level < nxt.cost + nxt.level

def reconstructPath(root):
    path = []
    while root:
        path.append(root.mat)
        root = root.parent
    return path[::-1]  # Reverse the path

def newNode(mat, empty_tile_pos, new_empty_tile_pos, level, parent, final):
    new_mat = copy.deepcopy(mat)
    x1, y1 = empty_tile_pos
    x2, y2 = new_empty_tile_pos
    new_mat[x1][y1], new_mat[x2][y2] = new_mat[x2][y2], new_mat[x1][y1]
    cost = heuristics.manhattan_distance(new_mat, final)
    return Node(parent, new_mat, new_empty_tile_pos, cost, level)

def branch_and_bound(initial_state, goal_state, empty_tile_pos):
    pq = priorityQueue()
    cost = heuristics.manhattan_distance(initial_state, goal_state)
    root = Node(None, initial_state, empty_tile_pos, cost, 0)
    pq.push(root)

    visited = set()
    visited.add(tuple(root.mat.reshape(-1)))

    while not pq.empty():
        min_node = pq.pop()
        if min_node.cost == 0:
            return reconstructPath(min_node)

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for move in moves:
            new_empty_pos = (min_node.empty_tile_pos[0] + move[0], min_node.empty_tile_pos[1] + move[1])
            if isSafe(new_empty_pos[0], new_empty_pos[1]):
                child = newNode(min_node.mat, 
                                min_node.empty_tile_pos, 
                                new_empty_pos, 
                                min_node.level + 1, 
                                min_node, 
                                goal_state)
                child_state_tuple = tuple(child.mat.reshape(-1))
                if child_state_tuple not in visited:
                    pq.push(child)
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