# This file contains code to implement a neural network that 
# will be used to create a heuristic to improve A* Search
# algorithm efficiency.

import numpy as np
import solver_helpers as sh

# A mechanism for one-hot encoding. A few key limitations:
#   - Max number of args is seven
#   - Max clause length is eight (discluding spaces)
#
# Returns an 8x8 numpy array. Rows represent different clauses
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
    for i in range(7 - len(encoded_state)): encoded_state.append(["00000000"]*8)

    # Add claim
    encoded_clause, literals = clause_encoding(claim, literals)
    encoded_state.append(encoded_clause)
    return np.array(encoded_state, dtype=object)
    

def clause_encoding(exp: str, literals: list) -> list:
    encoded_clause = []
    while exp != "":
        # Empty Space
        if exp[0:1] == ' ':
            exp = exp[1:len(exp)]

        # Operators
        elif exp[0:1] == ")":
            exp = exp[1:len(exp)]
            encoded_clause.append('10100000')
        elif exp[0:1] == "(":
            exp = exp[1:len(exp)]
            encoded_clause.append('11000000')
        elif exp[0:1] == "-": # '->' Operator
            exp = exp[2:len(exp)]
            encoded_clause.append('10000010')
        elif exp[0:1] == "|":
            exp = exp[1:len(exp)]
            encoded_clause.append('10000100')
        elif exp[0:1] == "&":
            exp = exp[1:len(exp)]
            encoded_clause.append('10001000')
        elif exp[0:1] == "~":
            exp = exp[1:len(exp)]
            encoded_clause.append('10010000')

        # Literals
        elif exp[0:1] in literals: # Literal already encountered
            idx = literals.index(exp[0:1])
            lit = "0"*(idx+1) + "1" + "0"*(6-idx)
            encoded_clause.append(lit)
            exp = exp[1:len(exp)]
        else: # New literal
            literals.append(exp[0:1]) # Add literal to list (encode next iteration)

    # Add row padding
    for i in range(8 - len(encoded_clause)): encoded_clause.append("00000000")
    return encoded_clause, literals

    