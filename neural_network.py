# This file contains code to implement a neural network that 
# will be used to create a heuristic to improve A* Search
# algorithm efficiency.

import numpy as np
import solver_helpers as sh
import random
import baseline_ai as baseline
import queue_search as qs
import a_star_heuristic as astar
import torch as tr
import matplotlib.pyplot as plt
import time

# A mechanism for one-hot encoding. A few key limitations:
#   - Max number of args is seven
#   - Max clause length is eight (discluding spaces)
#
# Returns an 16x8x8 tensor. Rows represent different clauses
# and columns represent different literals/operators/parens
# in an individual clause.
def one_hot_encoding(state: tuple):
    (args, claim, hist) = sh.unpack(state)

    encoded_state = []
    literals = []
    row = 0
    for clause in args:
        exp = clause
        
        # Helper function encodes clause
        encoded_clause, literals = clause_encoding(exp, literals)   
        encoded_state.append(encoded_clause)

    # Add column padding
    for i in range(15 - len(encoded_state)): 
        encoded_tmp = []
        for j in range(8):
            encoded_tmp.append([0,0,0,0,0,0,0,0])
        encoded_state.append(encoded_tmp)

    # Add claim
    encoded_clause, literals = clause_encoding(claim, literals)
    encoded_state.append(encoded_clause)
    return tr.tensor(encoded_state, dtype=tr.float32) # np.array(encoded_state, dtype=object)
    

# A helper method for one_hot_encoding that encodes a single
# clause (row) in the encoding.
def clause_encoding(exp: str, literals: list) -> list:
    encoded_clause = []
    while exp != "":
        # Empty Space
        if exp[0:1] == ' ':
            exp = exp[1:len(exp)]

        # Operators
        elif exp[0:1] == ")":
            exp = exp[1:len(exp)]
            encoded_clause.append([1,0,1,0,0,0,0,0])
        elif exp[0:1] == "(":
            exp = exp[1:len(exp)]
            encoded_clause.append([1,1,0,0,0,0,0,0])
        elif exp[0:1] == "-": # '->' Operator
            exp = exp[2:len(exp)]
            encoded_clause.append([1,0,0,0,0,0,1,0])
        elif exp[0:1] == "|":
            exp = exp[1:len(exp)]
            encoded_clause.append([1,0,0,0,0,1,0,0])
        elif exp[0:1] == "&":
            exp = exp[1:len(exp)]
            encoded_clause.append([1,0,0,0,1,0,0,0])
        elif exp[0:1] == "~":
            exp = exp[1:len(exp)]
            encoded_clause.append([1,0,0,1,0,0,0,0])

        # Literals
        elif exp[0:1] in literals: # Literal already encountered
            idx = literals.index(exp[0:1])
            lit = [0]*(idx+1) + [1] + [0]*(6-idx)
            encoded_clause.append(lit)
            exp = exp[1:len(exp)]
        else: # New literal
            literals.append(exp[0:1]) # Add literal to list (encode next iteration)

    # Add row padding
    for i in range(8 - len(encoded_clause)): encoded_clause.append([0,0,0,0,0,0,0,0])
    return encoded_clause, literals


# Generate training/testing data for the neural network
def generate_data(count=500) -> list:
    # Initial args (based on automated_experiments.py)
    arg_list = [["p -> q", "q -> r", "p", "q"],
                ["p -> q", "q -> r", "s & ~q", "~r"],
                ["p -> q", "~s & (q -> r)", "p", "t -> s"],
                ["p -> q", "r -> (p & q)", "r | s", "~s"],
                ["p -> (q -> s)", "s -> ~r", "p & q", "r | s"]]
    
    # Data list to populate
    state_list = []
    result_list = []

    while len(state_list) < count:
        args = random.choice(arg_list)

        # Generate the claim to prove by a series of random actions applied to args
        generation_state = sh.initial_state(args, "claim")
        (generation_state, x, y) = baseline.apply_random_actions(generation_state)
        claim = sh.unpack(generation_state)[0][-1]

        state = sh.initial_state(args, claim)        
        problem = qs.SearchProblem(state, sh.proof_complete)
        plan_astar, node_count_astar = qs.a_star_search(problem, astar.simple_heuristic)

        # Run entire problem
        states_astar = [problem.initial_state]
        for a in range(len(plan_astar)):
            states_astar.append(sh.apply_rule(plan_astar[a], states_astar[-1]))

        # Select random state to add as data
        data_idx = random.randint(0, len(states_astar)-1)
        state_data = states_astar[data_idx]
        label = (len(states_astar)-data_idx-1)

        # Append labeled data to list
        state_list.append(state_data)
        result_list.append(label)

    return state_list, result_list


def batch_error(net, batch):
    states, utilities = batch
    u = utilities.reshape(-1,1).float()
    y = net(states.float())
    e = tr.sum((y - u)**2) / utilities.shape[0]
    return e



# Note that train_nn() is written based on implementations
# from the following source.
#   Title:          ProjectExample.ipynb
#   Author:         Garrett Katz
#   Availability:   CIS 667, Lecture 12/05/2022
#   https://drive.google.com/file/d/1QF8IJHlZ597esIU-vmW7u9KARhyXIjOY/edit?pli=1

def train_nn():
    nn = tr.nn.Sequential(
        tr.nn.Linear(8, 640),
        tr.nn.ReLU(),
        tr.nn.Flatten(),
        tr.nn.Linear(81920, 64),
        tr.nn.MaxPool1d(64),
        tr.nn.ReLU()
    )

    optimizer = tr.optim.SGD(nn.parameters(), lr=1e-2)

    # Training Data
    print("\nCreating training data...\n")
    training_set = generate_data(count=500)
    states, utilities = training_set
    training_batch = tr.stack(tuple(map(one_hot_encoding, states))), tr.tensor(utilities)

    # Testing Data
    print("Creating testing data...\n")
    testing_set = generate_data(count=200)
    states, utilities = testing_set
    testing_batch = tr.stack(tuple(map(one_hot_encoding, states))), tr.tensor(utilities)

    # Run the gradient descent iterations
    print("Running gradient descent...\n")
    curves = [], []
    start = time.time()
    for epoch in range(250):
    
        optimizer.zero_grad()
        e = batch_error(nn, training_batch)
        e.backward()
        training_error = e.item()

        with tr.no_grad():
            e = batch_error(nn, testing_batch)
            testing_error = e.item()

        # Optimization step
        optimizer.step()    
        
        # Print/Save training progress
        if epoch % 1 == 0:
            end = time.time()
            print("%d: %f, %f, time elapsed: %f" % (epoch, training_error, testing_error, (end-start)))
        curves[0].append(training_error)
        curves[1].append(testing_error)

    # Remove data outlier (to make graph readable)
    curves[0].pop(1)
    curves[1].pop(1)

    # Plot learning curves
    plt.plot(curves[0], 'b-')
    plt.plot(curves[1], 'r-')
    plt.plot()
    plt.legend(["Train","Test"])
    plt.show()

    # Save torch model
    tr.save(nn, "saved_net.pt")

if __name__ == "__main__":
    train_nn()