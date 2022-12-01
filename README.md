# CIS 667: Logical Inference Proof Solver

# Installation

The only dependency for this project is PyTorch.

In order to run the Neural Networks leveraged by the advanced AI, download and install PyTorch (documentation available at https://pytorch.org/).


# Interactive Run

In a python enviornement, start run_solver.py.

First, select the methodology to use: 1. Human (choose which rules to apply), 2. Baseline AI (random selection), 3. Breadth First Search, 4. A* Search. (Enter the number corredsponding to the methodology as input.)

The program will prompt for a series of assumptions. When all have been entered, type 'DONE'. Any single character can act as a literal and the operators correspond to the following symbols:

- AND - '&'
- OR - '|'
- Implication - '->'
- Negation - '~'

The program will then prompt for a claim to prove.

The AI will then compute which inference rules need to be applied to the assumption set to reach the goal state (the claim that was entered). For the 'Human' methodology, you will be prompted to select a rule to apply based on valid actions in the given state. The other three methods are automated, but actions are triggered by pressing the 'Enter' key.

The output will be a formatted proof indicating which rules were applied to reach the final state.


# Computer Experiements

Automated computer experiments can be run using automated_experiments.py. These experiments compare the efficiency of three AI implementations: baseline (random selection), Breadth First Search, and A* Search. There are two options when running these experiments:

- To run full set of tests (5 batches of 100, increasing in complexity), set constant LIMITED_BATCHES to False. This version takes roughly fifteen minutes to run.
- To run set of tests with reduced batch sizes (specifically for the more complex problems), set constant LIMITED_BATCHES to true. This version runs in about two minutes.

The program will display a printed output of the average number of nodes used by each of the search algorithms, the number of steps each algorithm takes to reach the goal state, and the number of failures that the baseline AI has (as the number of actions are limited).


# Code Attributions

TODO: Find out proper formatting for this section
