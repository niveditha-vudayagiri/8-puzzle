# 8-Puzzle Solver

Welcome to the 8-Puzzle Solver project! This project implements various algorithms to solve the classic 8-puzzle problem. The implemented algorithms include BFS, DFID, and Bidirectional Search. Additionally, the project includes a visualization feature using Matplotlib and basic heuristic calculations.

<div style="text-align: center;">
    <img src="https://www.aiai.ed.ac.uk/~gwickler/images/8-puzzle-states.png" alt="8-Puzzle Image" width="300">
</div>

## Features

<ul style="list-style-type: circle;">
    <li>Implemented Algorithms:
        <ul>
            <li>Breadth-First Search (BFS)</li>
            <li>Depth-First Iterative Deepening (DFID)</li>
            <li>Bidirectional Search</li>
        </ul>
    </li>
    <li>Visualization of the solution path using Matplotlib</li>
    <li>Basic heuristic calculations (not used in algorithms but displayed)</li>
</ul>

## Installation
git clone https://github.com/your-username/8-puzzle.git
cd 8-puzzle

## Usage
You can run the main script to solve the puzzle using the desired algorithm and visualize the solution path. Here is an example of how to run the script:
python 8_puzzle_BFS.py

## Algorithms

### Breadth-First Search (BFS)
BFS explores all possible states level by level, ensuring the shortest path to the goal.

### Depth-First Iterative Deepening (DFID)
DFID combines the benefits of depth-first and breadth-first search, exploring deeper nodes iteratively.

### Bidirectional Search
Bidirectional Search runs two simultaneous searches: one forward from the initial state and one backward from the goal state, meeting in the middle to find the solution faster.

### Branch and Bound
An algorithm used to solve combinatorial optimization problems by systematically exploring branches of the search space, pruning branches that exceed the current best solution.

### Hill Climbing
A local search algorithm that starts with an arbitrary solution and iteratively makes small changes, moving to neighboring states with better objective values until no improvement is found.

### A*
A graph traversal and search algorithm that finds the shortest path from a start node to a goal node by combining the cost to reach the node and the estimated cost from the node to the goal (using a heuristic).

### Iterative Deepening A*
A variant of A* that performs a series of depth-first searches with increasing cost limits, combining the space efficiency of DFS with the optimality of A*.

### Best First Search
A search algorithm that explores a graph by expanding the most promising node chosen according to a specified rule or heuristic.

### Beam Search
A heuristic search algorithm that explores a graph by expanding the most promising nodes up to a fixed number of best candidates (beam width) at each level, balancing between breadth-first and depth-first search.

## Contributing
Feel free to fork this repository, make improvements, and submit pull requests. Contributions are welcome!
