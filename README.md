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

All automated testing is handled by test_solver.py. This program runs a series of unit tests that target specific aspects of the domain as well as several "black-box" test that provide input to the solver and validate the expected series of rules matches those taken by the AI to reach the goal state.


# Code Attributions

TODO: Find out proper formatting for this section
