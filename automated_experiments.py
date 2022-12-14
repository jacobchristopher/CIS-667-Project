import solver_helpers as sh
import rule_helpers as rh
import queue_search as qs
import a_star_heuristic as astar
import baseline_ai as baseline
import matplotlib.pyplot as plt
import numpy as np

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

LIMITED_BATCHES = False

class AutomatedExperiments:

    def run_experiment(args: list, claim_depth: int, baseline_depth: int, adv_heuristic) -> tuple:

        # Generate the claim to prove by a series of random actions applied to args
        generation_state = sh.initial_state(args, "claim")
        (generation_state, x, y) = baseline.apply_random_actions(generation_state, count=claim_depth)
        claim = sh.unpack(generation_state)[0][-1]

        state = sh.initial_state(args, claim)

        problem = qs.SearchProblem(state, sh.proof_complete)
        plan_bfs, node_count_bfs = qs.breadth_first_search(problem)
        plan_astar, node_count_astar = qs.a_star_search(problem, astar.simple_heuristic)
        plan_astar_nn, node_count_astar_nn = qs.a_star_search(problem, adv_heuristic)

        # -- Run AI --

        # BFS
        states_bfs = [problem.initial_state]
        for a in range(len(plan_bfs)):
            states_bfs.append(sh.apply_rule(plan_bfs[a], states_bfs[-1]))

        # A* Search (Simple)
        states_astar = [problem.initial_state]
        for a in range(len(plan_astar)):
            states_astar.append(sh.apply_rule(plan_astar[a], states_astar[-1]))

        # A* Search (Neural Net)
        states_astar_nn = [problem.initial_state]
        for a in range(len(plan_astar_nn)):
            states_astar_nn.append(sh.apply_rule(plan_astar_nn[a], states_astar_nn[-1]))


        # Baseline AI
        (state_baseline, solved, steps) = baseline.apply_random_actions(state, count=baseline_depth)

        return (states_bfs, node_count_bfs), (states_astar, node_count_astar), (state_baseline, steps, solved), (states_astar_nn, node_count_astar_nn)

def run_batch(args: list, formatted_title: str, claim_depth: int, baseline_depth = 100, batch_size = 100) -> tuple:
    # BFS Analysis
    node_count_bfs = 0
    node_dist_bfs = []
    # A* Analysis
    node_count_astar = 0
    node_dist_astar = []
    node_count_astar_nn = 0
    node_dist_astar_nn = []
    # General Search Analysis
    step_count_search = 0
    step_dist_search = []
    # Baseline Analysis
    step_count_baseline = 0
    baseline_failures = 0
    step_dist_baseline = []

    Net = astar.NeuralNetwork()
    adv = Net.nn_heuristic
    for i in range(batch_size):
        bfs, a_star, base, a_star_nn = AutomatedExperiments.run_experiment(args, claim_depth, baseline_depth, adv)
        # Node Counts
        node_count_bfs += bfs[1]
        node_count_astar += a_star[1]
        node_count_astar_nn += a_star_nn[1]
        # Step Counts
        step_count_baseline += base[1]
        step_count_search += len(bfs[0])
        # Distributions
        node_dist_bfs.append(bfs[1])
        node_dist_astar.append(a_star[1])
        node_dist_astar_nn.append(a_star_nn[1])
        step_dist_search.append(len(bfs[0]))
        step_dist_baseline.append(base[1])
        # Failures
        if not base[2]: baseline_failures += 1

    avg_node_bfs = node_count_bfs / batch_size
    avg_step_search = step_count_search /batch_size
    avg_node_astar = node_count_astar / batch_size
    avg_step_base = step_count_baseline / batch_size
    avg_node_astar_nn = node_count_astar_nn / batch_size

    print(formatted_title
          + str(avg_node_bfs) + ", " + str(avg_step_search) + print_padding(len(str(avg_node_bfs))+len(str(avg_step_search)))
          + "                     "
          + str(avg_node_astar) + ", " + str(avg_step_search) + print_padding(len(str(avg_node_astar))+len(str(avg_step_search)))
          + "                   "
          + str(avg_node_astar_nn) + ", " + str(avg_step_search) + print_padding(len(str(avg_node_astar_nn))+len(str(avg_step_search)))
          + "                   "
          + str(avg_step_base) + ", " + str(baseline_failures) + " failures" +"\n")

    return (node_dist_bfs, node_dist_astar, step_dist_search, step_dist_baseline, node_dist_astar_nn)


def create_experiment_histogram(data: tuple, label: str) -> None:
    # BFS Nodes
    bfs_dist = np.asarray(data[0])
    bfs_label = label + " BFS Node Distribution"
    plt.hist(bfs_dist)
    plt.title(bfs_label)
    plt.xlabel("Node Count")
    plt.show() 

    # A* Nodes
    astar_dist = np.asarray(data[1])
    astar_label = label + " A* Simple Node Distribution"
    plt.hist(astar_dist)
    plt.title(astar_label)
    plt.xlabel("Node Count")
    plt.show() 

    # Search Steps
    search_dist = np.asarray(data[2])
    search_label = label + " Search Algorithm Steps"
    plt.hist(search_dist)
    plt.title(search_label)
    plt.xlabel("Step Count")
    plt.show() 

    # Baseline Steps
    base_dist = np.asarray(data[3])
    base_label = label + " Baseline Algorithm Steps"
    plt.hist(base_dist)
    plt.title(base_label)
    plt.xlabel("Step Count")
    plt.show()

    # A* Nodes
    astar_dist = np.asarray(data[4])
    astar_label = label + " A* Neural Net Node Distribution"
    plt.hist(astar_dist)
    plt.title(astar_label)
    plt.xlabel("Node Count")
    plt.show() 



def print_padding(size: int) -> str:
    if size >= 10: return ("")
    elif size == 9: return (" ")
    elif size == 8: return ("  ")
    elif size == 7: return ("   ")
    elif size == 6: return ("    ")
    elif size == 5: return ("     ")
    elif size == 4: return ("      ")
    else: return ("       ")


if __name__ == "__main__":

    print("\n             BFS (nodes, steps)  |  A* Simple (nodes, steps)  |  A* Neural Net (nodes, steps)  |  Baseline AI (steps, failures) \n")
    print("----------------------------------------------------------------------------------------------------------------------------------- \n")

    # -- Smallest Experiment --
    smallest_args = ["p -> q", "q -> r", "p", "q"]
    str_smallest = "Smallest:       "           
    smallest_dist = run_batch(smallest_args, str_smallest, 10)

    # -- Small Experiment --
    small_args = ["p -> q", "q -> r", "s & ~q", "~r"]
    str_small = "Small:          "
    small_dist = run_batch(smallest_args, str_small, 50)

    # -- Medium Experiment --
    medium_args = ["p -> q", "~s & (q -> r)", "p", "t -> s"]
    str_medium = "Medium:         "
    if LIMITED_BATCHES: medium_dist = run_batch(medium_args, str_medium, 100, baseline_depth=200, batch_size=50)
    else: medium_dist = run_batch(medium_args, str_medium, 100, baseline_depth=200)

    # -- Large Experiment --
    large_args = ["p -> q", "r -> (p & q)", "r | s", "~s"]
    str_large = "Large:          "
    if LIMITED_BATCHES: large_dist = run_batch(large_args, str_large, 100, baseline_depth=200, batch_size=20)
    else: large_dist = run_batch(large_args, str_large, 100, baseline_depth=200)

    # -- Largest Experiment --
    largest_args = ["p -> (q -> s)", "s -> ~r", "p & q", "r | s"]
    str_largest = "Largest:        "
    if LIMITED_BATCHES: largest_dist = run_batch(largest_args, str_largest, 200, baseline_depth=300, batch_size=5)
    else: largest_dist = run_batch(largest_args, str_largest, 200, baseline_depth=300)

    # -- Histogram Generator --
    create_experiment_histogram(smallest_dist, "Smallest")
    create_experiment_histogram(small_dist, "Small")
    create_experiment_histogram(medium_dist, "Medium")
    create_experiment_histogram(large_dist, "Large")
    create_experiment_histogram(largest_dist, "Largest")