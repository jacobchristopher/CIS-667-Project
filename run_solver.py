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
    
    # print ("==> BFS BEGIN")
    plan, node_count = breadth_first_search(problem)
    # print ("==> BFS DONE")
    # plan, node_count = a_star_search(problem, domain.simple_heuristic)

    states = [problem.initial_state]
    for a in range(len(plan)):
        states.append(sh.apply_rule(plan[a], states[-1]))

    # Display final proof
    # print(states)
    final_state = states[len(states)-1]
    # print(final_state)
    (args, claim, hist) = sh.unpack(final_state)
    start_rule = hist[0][2]
    hist_index = 0
    for i in range(len(args)):
        rule = "Assumption"
        if i >= start_rule:
            rule = str(hist[hist_index][0])
            rule += " "
            rule += str(tuple(map(lambda i: i + 1, hist[hist_index][1])))
            hist_index += 1
        print(str(i+1) + ". " + args[i] + "     " + rule +"\n")