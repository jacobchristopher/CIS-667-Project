import solver_helpers as sh
import rule_helpers as rh
import queue_search as qs
import a_star_heuristic as astar
import baseline_ai as baseline

# This is an automated testing file that generates random claims to prove for
# each of the three AI types: baseline (random), BFS, and A* Search.

# The generation of these random claims is relatively expensive. So are the
# tests (specifically for the baseline AI), so runtime can be several minutes.
# To reduce time of runs, modify problem sizes in main (namely the claim_depth
# and baseline_depth variabels of run_batch function).

# Lowering the claim_depth will make the claims easier for the AI to prove.
# Lowering the baseline_depth will result in more baseline AI failures, but
# will reduce the runtime (as this limits the number of actions the AI takes).

# Finally, runtime can be imrpoved by limiting batch sizes. Change the constant
# below to True for version that runs in under two minutes. Change the constant
# below to False for full version (batch sizes of 100).

LIMITED_BATCHES = True

class AutomatedExperiments:

    def run_experiment(args: list, claim_depth: int, baseline_depth: int):

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

def run_batch(args: list, formatted_title: str, claim_depth: int, baseline_depth = 100, batch_size = 100):
    node_count_bfs = 0
    step_count_bfs = 0
    node_count_astar = 0
    step_count_astar = 0
    step_count_baseline = 0
    baseline_failures = 0

    for i in range(batch_size):
        bfs, a_star, base = AutomatedExperiments.run_experiment(args, claim_depth, baseline_depth)
        node_count_bfs += bfs[1]
        step_count_bfs += len(bfs[0])
        node_count_astar += a_star[1]
        step_count_astar += len(a_star[0])
        step_count_baseline += base[1]
        if not base[2]: baseline_failures += 1

    avg_node_bfs = node_count_bfs / batch_size
    avg_step_bfs = step_count_bfs /batch_size
    avg_node_astar = node_count_astar / batch_size
    avg_step_astar = step_count_astar / batch_size
    avg_step_base = step_count_baseline / batch_size

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
    small_args = ["p -> q", "q -> r", "s & ~q", "~r"]
    run_batch(smallest_args, "Small:                  ", 50)

    # -- Medium Experiment --
    medium_args = ["p -> q", "~s & (q -> r)", "p", "t -> s"]
    if LIMITED_BATCHES: run_batch(medium_args, "Medium:                 ", 100, baseline_depth=200, batch_size=50)
    else: run_batch(medium_args, "Medium:                 ", 100, baseline_depth=200)

    # -- Large Experiment --
    large_args = ["p -> q", "r -> (p & q)", "r | s", "~s"]
    if LIMITED_BATCHES: run_batch(large_args, "Large:                  ", 100, baseline_depth=200, batch_size=20)
    else: run_batch(large_args, "Large:                  ", 100, baseline_depth=200)

    # -- Largest Experiment --
    largest_args = ["p -> (q -> s)", "s -> ~r", "p & q", "r | s"]
    if LIMITED_BATCHES: run_batch(largest_args, "Largest:                ", 200, baseline_depth=300, batch_size=5)
    else: run_batch(largest_args, "Largest:                ", 200, baseline_depth=300)