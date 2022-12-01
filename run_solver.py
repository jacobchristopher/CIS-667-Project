import solver_helpers as sh
import rule_helpers as rh
from queue_search import *
import a_star_heuristic as astar
import baseline_ai as baseline

def read_arg_input() -> tuple:
    print("------ Welcome to Logical Inference Solver ------\n")
    print("Follow the prompts to begin.\n")
    
    print("Enter the number corresponding to the AI you would like to use: \n")
    print("      1. Human (You select actions)   2. Baseline AI (Random) \n" +
          "      3. Breadth First Search         4. A* Search            \n ")
    method = input()
    print("\n")
    next_arg = ""
    arg_list = []
    while not next_arg == "DONE":
        next_arg = input('Enter the next logical assumption (or type \'DONE\' if complete):\n') 
        arg_list.append(next_arg)
        print("\n")
    arg_list.pop()      # Remove 'DONE' from list
    claim = input('Enter the claim to prove:\n')
    print("\n-----------------------------------------------\n")
    return(arg_list, claim, method)


if __name__ == "__main__":
    (args, claim, method) = read_arg_input()
    state = sh.initial_state(args, claim)
    problem = SearchProblem(state, sh.proof_complete)

    if method == '1':
        for i in range(len(args)):
            rule = "Assumption"
            print(str(i+1) + ". " + args[i] + "     " + rule +"\n")
        print("\n-----------------------------------------------\n")
        while not sh.proof_complete(state):
            actions = sh.valid_actions(state)
            i = 1
            for x in actions:
                print(str(i) + ". " + str(x))
                i += 1
            print("\n")
            act_idx = input("Select rule number to apply:\n")
            state = sh.apply_rule(actions[int(act_idx) - 1], state)
            print("\n-----------------------------------------------\n")
            (args, claim, hist) = sh.unpack(state)
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

            
    elif method == '2':
        (state, success, steps) = baseline.apply_random_actions(state)
        # Display final proof
        (args, claim, hist) = sh.unpack(state)
        start_rule = hist[0][2]
        hist_index = 0
        for i in range(len(args)):
            rule = "Assumption"
            if i >= start_rule:
                input()
                rule = str(hist[hist_index][0])
                rule += " "
                rule += str(tuple(map(lambda i: i + 1, hist[hist_index][1])))
                hist_index += 1
            print(str(i+1) + ". " + args[i] + "     " + rule +"\n")

    else:
    
        if method == '3': plan, node_count = breadth_first_search(problem)
        else: plan, node_count = a_star_search(problem, astar.simple_heuristic)

        states = [problem.initial_state]
        for a in range(len(plan)):
            states.append(sh.apply_rule(plan[a], states[-1]))

        # Display final proof
        final_state = states[len(states)-1]
        (args, claim, hist) = sh.unpack(final_state)
        start_rule = hist[0][2]
        hist_index = 0
        for i in range(len(args)):
            rule = "Assumption"
            if i >= start_rule:
                input()
                rule = str(hist[hist_index][0])
                rule += " "
                rule += str(tuple(map(lambda i: i + 1, hist[hist_index][1])))
                hist_index += 1
            print(str(i+1) + ". " + args[i] + "     " + rule +"\n")