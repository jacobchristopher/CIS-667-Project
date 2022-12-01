# CIS 667: Logical Inference Proof Solver

# Installation

The only dependency for this project is PyTorch.

In order to run the Neural Networks leveraged by the advanced AI, download and install PyTorch (documentation available at https://pytorch.org/).


# Interactive Run

In a python enviornement, start run_solver.py.

The program will prompt for a series of assumptions. When all have been entered, type 'DONE'.

The program will then prompt for a conclusion to prove.

The AI will then compute which inference rules need to be applied to the assumption set to reach the goal state (the claim that was entered).

The output will be a formatted proof indicating which rules were applied to reach the final state.


# Computer Experiements

Automated computer experiments can be run using automated_experiments.py. These experiments compare the efficiency of three AI implementations: baseline (random selection), Breadth First Search, and A* Search. There are two options when running these experiments:

- To run full set of tests (5 batches of 100, increasing in complexity), set constant LIMITED_BATCHES to False. This version takes roughly an hour to finish.
- To run set of tests with reduced batch sizes (specifically for the more complex problems), set constant LIMITED_BATCHES to true. This version runs in under five minutes.

The program will display a printed output of the average number of nodes used by each of the search algorithms, the number of steps each algorithm takes to reach the goal state, and the number of failures that the baseline AI has (as the number of actions are limited).


# Code Attributions

TODO: Find out proper formatting for this section
