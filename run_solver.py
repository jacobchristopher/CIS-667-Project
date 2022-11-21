import solver_helpers as sh
import rule_helpers as rh
from queue_search import *

def read_arg_input() -> tuple:
    print("------ Welcome to Logical Inference Solver ------\n")
    print("Follow the prompts to begin.\n")
    next_arg = ""
    arg_list = []
    while not next_arg == "DONE":
        next_arg = input('Enter the next logical assumption (or type \'DONE\' if complete):\n') 
        arg_list.append(next_arg)
        print("\n")
    arg_list.pop()      # Remove 'DONE' from list
    claim = input('Enter the claim to prove:\n')
    print("\n-----------------------------------------------\n")
    return(arg_list, claim)


if __name__ == "__main__":
    (args, claim) = read_arg_input()
    state = sh.initial_state(args, claim)

    problem = SearchProblem(state, sh.proof_complete)
    
    plan, node_count = breadth_first_search(problem)
    # plan, node_count = a_star_search(problem, domain.simple_heuristic)

    states = [problem.initial_state]
    for a in range(len(plan)):
        states.append(sh.apply_rule(plan[a], states[-1]))

    print(states)