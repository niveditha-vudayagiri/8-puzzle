import copy
import heuristics
import numpy as np
import heapq
import visualise_puzzle as vis
import heuristics

class Node:
    def __init__(self, parent, mat, empty_tile_pos, g_cost, h_cost):
        self.parent = parent
        self.mat = mat
        self.empty_tile_pos = empty_tile_pos
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    @staticmethod
    def reconstruct_path(node):
        path = []
        while node:
            path.append(node.mat)
            node = node.parent
        return path[::-1]

    @staticmethod
    def new_node(mat, empty_tile_pos, new_empty_tile_pos, g_cost, parent, final):
        new_mat = copy.deepcopy(mat)
        x1, y1 = empty_tile_pos
        x2, y2 = new_empty_tile_pos
        new_mat[x1][y1], new_mat[x2][y2] = new_mat[x2][y2], new_mat[x1][y1]
        h_cost = heuristics.manhattan_distance(new_mat, final)
        return Node(parent, new_mat, new_empty_tile_pos, g_cost, h_cost)
    

def is_safe(x, y):
    return 0 <= x < 3 and 0 <= y < 3

def a_star(start, goal):
    open_list = []
    closed_list = set()
    start_node = Node(None, start, tuple(np.argwhere(start == 0)[0]), 0, heuristics.manhattan_distance(start, goal))
    goal_node = Node(None, goal, tuple(np.argwhere(goal == 0)[0]), 0, 0)
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if np.array_equal(current_node.mat, goal_node.mat):
            return Node.reconstruct_path(current_node)

        closed_list.add(tuple(current_node.mat.reshape(-1)))

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for move in moves:
            new_empty_pos = (current_node.empty_tile_pos[0] + move[0], current_node.empty_tile_pos[1] + move[1])
            if is_safe(new_empty_pos[0], new_empty_pos[1]):
                child = Node.new_node(current_node.mat, 
                                      current_node.empty_tile_pos, 
                                      new_empty_pos, 
                                      current_node.g_cost + 1, 
                                      current_node, 
                                      goal)
                child_state_tuple = tuple(child.mat.reshape(-1))

                if child_state_tuple in closed_list:
                    continue

                in_open_list = False
                for open_node in open_list:
                    if np.array_equal(open_node.mat, child.mat):
                        in_open_list = True
                        if child.g_cost < open_node.g_cost:
                            open_node.g_cost = child.g_cost
                            open_node.f_cost = child.f_cost
                            open_node.parent = child.parent
                        break

                if not in_open_list:
                    heapq.heappush(open_list, child)
                    closed_list.add(child_state_tuple)
                    
    return None

if __name__ == "__main__":
    initial_state = np.array([[1, 4, 3], [2, 5, 6], [8, 7, 0]])
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    empty_tile_pos = tuple(np.argwhere(initial_state == 0)[0])

    solution_path = a_star(initial_state, goal_state)

    if solution_path:
        vis.visualize_puzzle(solution_path, goal_state)
        print("Goal state reached!")
    else:
        print("No solution found.")