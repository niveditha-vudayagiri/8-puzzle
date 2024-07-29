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

# Breadth-First Search (BFS)
BFS explores all possible states level by level, ensuring the shortest path to the goal.

# Depth-First Iterative Deepening (DFID)
DFID combines the benefits of depth-first and breadth-first search, exploring deeper nodes iteratively.

# Bidirectional Search
Bidirectional Search runs two simultaneous searches: one forward from the initial state and one backward from the goal state, meeting in the middle to find the solution faster.

## Contributing
Feel free to fork this repository, make improvements, and submit pull requests. Contributions are welcome!
