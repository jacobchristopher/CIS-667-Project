import solver_helpers as sh
import rule_helpers as rh
import neural_network as nn
import torch as tr

# A baseline heuristic for A* Search
def simple_heuristic(state: tuple) -> int:
    (args, claim, hist) = sh.unpack(state)
    parsed_claim = rh.parse_expression(claim)
    a = parsed_claim[1]
    b = parsed_claim[2]
    advanced_conclusion = False
    if b != "": advanced_conclusion = True

    steps = 0
    if a not in args: steps += 1
    if advanced_conclusion:
        if b not in args: steps += 1

    return steps

# An advnaced heuristic using trained neural network
def nn_heuristic(state: tuple) -> int:
    # Load net
    net = tr.load("saved_net.pt")
    # Get heuristic value
    steps = net(tr.stack(tuple(map(nn.one_hot_encoding, [state]))))
    return steps
