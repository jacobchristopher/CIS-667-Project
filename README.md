# CIS 667: Logical Inference Proof Solver

# Installation

There are three dependencies for this project:

- NumPy
- MatPlotLib
- PyTorch

NumPy and MatPlotLib are utilized for automated testing. Download and install NumPy (documentation available at https://numpy.org/). Download and install MatPlotLib (documentation available at https://matplotlib.org/).

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

- To run full set of tests (5 batches of 100, increasing in complexity), set constant LIMITED_BATCHES to False. This version takes roughly ten minutes to run.
- To run set of tests with reduced batch sizes (specifically for the more complex problems), set constant LIMITED_BATCHES to true. This version runs in about two minutes.

The program will display a printed output of the average number of nodes used by each of the search algorithms, the number of steps each algorithm takes to reach the goal state, and the number of failures that the baseline AI has (as the number of actions are limited). It will also generate histogram plots for the node and step counts that are displayed. Certain information can be gathered from the analysis of these:

- BFS Node Count Distribution and A* Search Node Count Distribution can be compared to analyze the efficiency of the heuristic used.
- Search Algorithm Step Distribution will be indicative of the problem complexity of the randomly generate proofs at a given problem size (as it shows the minimum number of steps to prove the claim).
- Baseline Algorithm Step Distribution shows how much worse the randomized AI performs at solving these proofs, demonstrating the value of using a search tree algorithm.


# Code Attributions

The files queue_search.py and sections of test_solver.py levarage implementations from the following sources:

Hunter, J. D. "Matplotlib: A 2D Graphics Environment." Computing in Science & Engineering, vol. 9, no. 3, 2007, pp. 90-95.

Harris, C.R., Millman, K.J., et al. Array programming with NumPy. Nature 585, 2020, pp. 357–362. https://doi.org/10.1038/s41586-020-2649-2

Katz, Garrett. "queue_search_code.py." Homework 01. CIS 667, Fall 2022.

Katz, Garrett. "roomba_heuristic_test.py." Homework 01. CIS 667, Fall 2022.

Newell, A., et al. “Empirical explorations of the logic theory machine: a case study in heuristic.” Western Joint Computer Conference: Techniques for reliability, February 26-28, 1957. Association for Computing Machinery, New York, NY, USA, pp. 218–230, February 26, 1957. https://doi.org/10.1145/1455567.1455605

Paszke, A., Gross, S., et al. PyTorch: An Imperative Style, High-Performance Deep Learning Library. Advances in Neural Information Processing Systems 32, Curran Associates, Inc., pp. 8024–8035. http://papers.neurips.cc/paper/9015-pytorch-an-imperative-style-high-performance-deep-learning-library.pdf