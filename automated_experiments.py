import solver_helpers as sh
import rule_helpers as rh
import queue_search as qs
import a_star_heuristic as astar
import baseline_ai as baseline

class AutomatedExperiments:

    # Consolidate into one utility method for all sizes
    # Input will be args and depth of conclusion (to be randomly generated)

    def run_experiment(args: list, claim_depth: int, baseline_depth: int):
        # -- Setup --

        # Generate the claim to prove by a series of random actions applied to args
        generation_state = sh.initial_state(args, "claim")
        (generation_state, x, y) = baseline.apply_random_actions(generation_state, count=claim_depth)
        claim = sh.unpack(generation_state)[0][-1]

        state = sh.initial_state(args, claim)

        problem = qs.SearchProblem(state, sh.proof_complete)
        plan_bfs, node_count_bfs = qs.breadth_first_search(problem)
        plan_astar, node_count_astar = qs.a_star_search(problem, astar.simple_heuristic)

        # -- Run AI --

        # BFS
        states_bfs = [problem.initial_state]
        for a in range(len(plan_bfs)):
            states_bfs.append(sh.apply_rule(plan_bfs[a], states_bfs[-1]))

        # A* Search
        states_astar = [problem.initial_state]
        for a in range(len(plan_astar)):
            states_astar.append(sh.apply_rule(plan_astar[a], states_astar[-1]))

        # Baseline AI
        (state_baseline, solved, steps) = baseline.apply_random_actions(state, count=baseline_depth)

        return (states_bfs, node_count_bfs), (states_astar, node_count_astar), (state_baseline, steps, solved)

def run_batch(args: list, formatted_title: str, claim_depth: int, baseline_depth = 100):
    node_count_bfs = 0
    step_count_bfs = 0
    node_count_astar = 0
    step_count_astar = 0
    step_count_baseline = 0
    baseline_failures = 0

    for i in range(100):
        bfs, a_star, base = AutomatedExperiments.run_experiment(args, claim_depth, baseline_depth)
        node_count_bfs += bfs[1]
        step_count_bfs += len(bfs[0])
        node_count_astar += a_star[1]
        step_count_astar += len(a_star[0])
        step_count_baseline += base[1]
        # step_count_baseline += int(base[2]==True) * base[1]
        if not base[2]: baseline_failures += 1

    avg_node_bfs = node_count_bfs / 100
    avg_step_bfs = step_count_bfs /100
    avg_node_astar = node_count_astar / 100
    avg_step_astar = step_count_astar /100
    avg_step_base = step_count_baseline / 100

    print(formatted_title
          + str(avg_node_bfs) + ", " + str(avg_step_bfs) + print_padding(len(str(avg_node_bfs))+len(str(avg_step_bfs)))
          + "                              "
          + str(avg_node_astar) + ", " + str(avg_step_astar) + print_padding(len(str(avg_node_astar))+len(str(avg_step_astar)))
          + "                            "
          + str(avg_step_base) + ", " + str(baseline_failures) + " failures" +"\n")

def print_padding(size: int):
    if size >= 10: return ("")
    elif size == 9: return (" ")
    elif size == 8: return ("  ")
    elif size == 7: return ("   ")
    elif size == 6: return ("    ")
    elif size == 5: return ("     ")
    elif size == 4: return ("      ")
    else: return ("       ")


if __name__ == "__main__":

    print("\n                 BFS Node Count (nodes, steps)            A* Node Count (nodes, steps)            Baseline AI (steps, failures) \n")
    print("----------------------------------------------------------------------------------------------------------------------------------- \n")

    # -- Smallest Experiment --
    smallest_args = ["p -> q", "q -> r", "p", "q"]
    run_batch(smallest_args, "Smallest:               ", 10)

    # -- Small Experiment --
    small_args = ["p -> q", "q -> r", "p & q"]
    run_batch(smallest_args, "Small:                  ", 100, 200)

    # -- Medium Experiment --
    medium_args = ["p -> q", "q -> r", "p & q", "r | s"]
    run_batch(medium_args, "Medium:                 ", 250, 500)

    # -- Large Experiment --
    large_args = ["p -> q", "q -> r", "p & q", "r | s"]
    run_batch(large_args, "Large:                  ", 500, 1000)

    # -- Largest Experiment --
    largest_args = ["p -> q", "q -> r", "p & q", "r | s"]
    run_batch(largest_args, "Largest:                ", 750, 1500)