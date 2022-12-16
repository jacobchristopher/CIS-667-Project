import heapq as hq
from collections import deque
import solver_helpers as sh
import rule_helpers as rh

# Note that the queue search code below is written based
# on function implementations from the following source.
#   Title:          queue_search_code.py
#   Author:         Garrett Katz
#   Availability:   CIS 667, Homework 01

class SearchNode(object):
    def __init__(self, problem, state, parent=None, action=None, step_cost=0, depth=0):
        self.problem = problem
        self.state = state
        self.parent = parent
        self.action = action
        self.step_cost = step_cost
        self.path_cost = step_cost + (0 if parent is None else parent.path_cost)
        self.path_risk = self.path_cost + problem.heuristic(state)
        self.depth = depth
        self.child_list = []
    def is_goal(self):
        return self.problem.is_goal(self.state)
    def children(self):
        if len(self.child_list) > 0: return self.child_list
        for action in sh.valid_actions(self.state):
            new_state = sh.apply_rule(action, self.state)
            self.child_list.append(
                SearchNode(self.problem, new_state, self, action, 1, depth=self.depth+1))
        return self.child_list
    def path(self):
        if self.parent == None: return []
        return self.parent.path() + [self.action]

class SearchProblem(object):
    def __init__(self, initial_state, is_goal = None):
        if is_goal is None: is_goal = lambda s: False
        self.initial_state = initial_state
        self.is_goal = is_goal
        self.heuristic = lambda s: 0
    def root_node(self):
        return SearchNode(self, self.initial_state)

class FIFOFrontier:
    def __init__(self):
        self.queue_nodes = deque()
        self.queue_states = set()
    def __len__(self):
        return len(self.queue_states)
    def push(self, node):
        if node.state not in self.queue_states:
            self.queue_nodes.append(node)
            self.queue_states.add(node.state)
    def pop(self):
        node = self.queue_nodes.popleft()
        self.queue_states.remove(node.state)
        return node
    def is_not_empty(self):
        return len(self.queue_nodes) > 0

class PriorityHeapFIFOFrontier(object):
    def __init__(self):
        self.heap = []
        self.state_lookup = {}
        self.count = 0

    def push(self, node):
        if node.state in self.state_lookup:
            entry = self.state_lookup[node.state]
            if entry[0] <= node.path_risk: return
            entry[-1] = True
        new_entry = [node.path_risk, self.count, node, False]
        hq.heappush(self.heap, new_entry)
        self.state_lookup[node.state] = new_entry
        self.count += 1

    def pop(self):
        while len(self.heap) > 0:
            risk, count, node, already_removed = hq.heappop(self.heap)
            if not already_removed:
                self.state_lookup.pop(node.state)
                return node

    def is_not_empty(self):
        return len(self.heap) > 0

    def states(self):
        return list(self.state_lookup.keys())

def queue_search(frontier, problem):
    node_count = 0
    explored = set()
    root = problem.root_node()
    frontier.push(root)
    while frontier.is_not_empty():
        node = frontier.pop()
        node_count += 1
        if node.is_goal(): break
        explored.add(node.state)
        for child in node.children():
            if child.state in explored: continue
            frontier.push(child)
    plan = node.path() if node.is_goal() else []

    return plan, node_count

def breadth_first_search(problem):
    return queue_search(FIFOFrontier(), problem)

def a_star_search(problem, heuristic):
    problem.heuristic = heuristic
    return queue_search(PriorityHeapFIFOFrontier(), problem)