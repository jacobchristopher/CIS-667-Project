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

# Encapsulate this in a class so that net is only
# loaded once
class NeuralNetwork:
    def __init__(self):
        self.net = tr.load("saved_net.pt")

    # An advnaced heuristic using trained neural network
    def nn_heuristic(self, state: tuple) -> int:
        # Get heuristic value
        steps = self.net(tr.stack(tuple(map(nn.one_hot_encoding, [state]))))
        return steps
