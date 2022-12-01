import unittest as ut
import solver_helpers as sh
import rule_helpers as rh
import queue_search as qs
import a_star_heuristic as astar

class HelperTestCase(ut.TestCase):

    def test_initial_state(self):
        args = ["p -> q", "p"]
        claim = "q"
        state  = sh.initial_state(args, claim)
        expected_state = sh.pack(args, claim, [])
        self.assertEqual(state, expected_state)

    def test_proof_complete(self):
        args = ["p -> q", "p"]
        claim = "q"
        args.append(claim)
        state = sh.pack(args, claim, [])
        self.assertTrue(sh.proof_complete(state))
    
    def test_proof_incomplete(self):
        args = ["p -> q", "p"]
        claim = "q"
        state = sh.pack(args, claim, [])
        self.assertFalse(sh.proof_complete(state))

    def test_valid_actions(self):
        args = ["p -> q", "p"]
        claim = "q"
        state = sh.pack(args, claim, [])
        applic = sh.valid_actions(state)
        exp = [(('Modus Ponens',['a', 'a -> b'], 'b'), [(1, 0), (0, 1)], 'p', 'q'),
               (('Conjunction', ['a', 'b'], 'a & b'), [(1, 0), (1, 0)], 'p', 'p')]
        self.assertEqual(applic, exp)

    def test_apply_rule_MP(self):
        args = ["p -> q", "p"]
        claim = "q"
        state = sh.pack(args, claim, [])
        applic = sh.valid_actions(state)
        exp = sh.pack(["p -> q", "p", "q"], claim, [("Modus Ponens", (1,0), 2)])
        state = sh.apply_rule(applic[0], state)
        self.assertEqual(state, exp)
        self.assertTrue(sh.proof_complete(state))


class RuleTestCase(ut.TestCase):

    def test_simple_imp_parse(self):
        arg = "p -> q"
        ans = rh.parse_expression(arg)
        exp = ("a -> b", "p", "q")
        self.assertEqual(ans, exp)

    def test_simple_and_parse(self):
        arg = "p * q"
        ans = rh.parse_expression(arg)
        exp = ("a * b", "p", "q")
        self.assertEqual(ans, exp)

    def test_paren_parse(self):
        arg = "(p * r) -> q"
        ans = rh.parse_expression(arg)
        exp = ("a -> b", "(p * r)", "q")
        self.assertEqual(ans, exp)

    def test_mult_paren_parse(self):
        arg = "(p * r) | (q -> r)"
        ans = rh.parse_expression(arg)
        exp = ("a | b", "(p * r)", "(q -> r)")
        self.assertEqual(ans, exp)

    def test_negation_parse(self):
        arg = "~p -> ~r"
        ans = rh.parse_expression(arg)
        exp = ("~a -> ~b", 'p', 'r')
        self.assertEqual(ans, exp)

    def test_applicable_rules1(self):
        args = ["p -> q", "p"]
        claim = "q"
        state = sh.pack(args, claim, [])
        applic = rh.applicable_rules(state)
        exp = [(('Modus Ponens', ['a', 'a -> b'], 'b'), [(1, 0), (0, 1)], 'p', 'q'),
               (('Conjunction', ['a', 'b'], 'a & b'), [(1, 0), (1, 0)], 'p', 'p')]
        self.assertEqual(applic, exp)

    def test_applicable_rules2(self):
        args = ["p -> q", "p", "x -> y", "x"]
        claim = "q"
        state = sh.pack(args, claim, [])
        applic = rh.applicable_rules(state)
        exp = [(('Modus Ponens', ['a', 'a -> b'], 'b'), [(1, 0), (0, 1)], 'p', 'q'), 
               (('Modus Ponens', ['a', 'a -> b'], 'b'), [(3, 0), (2, 1)], 'x', 'y'),
               (('Conjunction', ['a', 'b'], 'a & b'), [(1, 0), (1, 0)], 'p', 'p'),
               (('Conjunction', ['a', 'b'], 'a & b'), [(1, 0), (3, 0)], 'p', 'x'),
               (('Conjunction', ['a', 'b'], 'a & b'), [(3, 0), (1, 0)], 'x', 'p'),
               (('Conjunction', ['a', 'b'], 'a & b'), [(3, 0), (3, 0)], 'x', 'x')]
        self.assertEqual(applic, exp)

    def test_applicable_rules3(self):
        args = ["p", "p -> q", "q -> r"]
        claim = "r"
        state = sh.pack(args, claim, [])
        applic = rh.applicable_rules(state)
        exp = [(('Modus Ponens', ['a', 'a -> b'], 'b'), [(0,0), (1,1)], 'p', 'q'),
               (('Conjunction', ['a', 'b'], 'a & b'), [(0, 0), (0, 0)], 'p', 'p'),
               (('Hypothetical Syllogism', ['a -> b'], 'a -> b'), [(1, 0), (2, 0)], 'p', 'r')]
        self.assertEqual(applic, exp)

    def test_applicable_rules4(self):
        args = ["p -> q", "q -> r", "p", "r -> s"]
        claim = "s"
        state = sh.pack(args, claim, [])
        applic = rh.applicable_rules(state)
        exp = [(('Modus Ponens', ['a', 'a -> b'], 'b'), [(2,0), (0,1)], 'p', 'q'),
               (('Conjunction', ['a', 'b'], 'a & b'), [(2, 0), (2, 0)], 'p', 'p'),
               (('Hypothetical Syllogism', ['a -> b'], 'a -> b'), [(0, 0), (1, 0)], 'p', 'r'),
               (('Hypothetical Syllogism', ['a -> b'], 'a -> b'), [(1, 0), (3, 0)], 'q', 's')]
        self.assertEqual(applic, exp)


class RuleDictTestCase(ut.TestCase):

    def test_conjunction_rule(self):
        args = ["p", "q"]
        claim = "p & q"
        state = sh.pack(args, claim, [])
        applic = rh.applicable_rules(state)
        exp = [(('Conjunction', ['a', 'b'], 'a & b'), [(0, 0), (0, 0)], 'p', 'p'), 
               (('Conjunction', ['a', 'b'], 'a & b'), [(0, 0), (1, 0)], 'p', 'q'), 
               (('Conjunction', ['a', 'b'], 'a & b'), [(1, 0), (0, 0)], 'q', 'p'), 
               (('Conjunction', ['a', 'b'], 'a & b'), [(1, 0), (1, 0)], 'q', 'q')]
        self.assertEqual(applic, exp)

    def test_modus_ponens_rule(self):
        args = ["p", "p -> q"]
        claim = "q"
        state = sh.pack(args, claim, [])
        applic = rh.applicable_rules(state)
        exp = [(('Modus Ponens', ['a', 'a -> b'], 'b'), [(0,0), (1,1)], 'p', 'q'),
               (('Conjunction', ['a', 'b'], 'a & b'), [(0, 0), (0, 0)], 'p', 'p')]
        self.assertEqual(applic, exp)

    def test_simplification_rule(self):
        args = ["p & q"]
        claim = "q"
        state = sh.pack(args, claim, [])
        applic = rh.applicable_rules(state)
        exp = [(('Simplification', ['a & b'], 'a'), [(0,0)], 'p', 'q'), 
               (('Simplification', ['a & b'], 'b'), [(0,0)], 'p', 'q')]
        self.assertEqual(applic, exp)

    def test_disjunctive_syllogism_rule(self):
        args = ["p | q", "~p"]
        claim = "q"
        state = sh.pack(args, claim, [])
        applic = rh.applicable_rules(state)
        exp = [(('Disjunctive Syllogism', ['a | b', '~a'], 'b'), [(0, 0), (1, 1)], 'p', 'q')]
        self.assertEqual(applic, exp)

    def test_mult_implication_rule(self):
        args = ["p -> q", "p -> r", "p"]
        claim = "q"
        state = sh.pack(args, claim, [])
        applic = rh.applicable_rules(state)
        exp = [(('Modus Ponens', ['a', 'a -> b'], 'b'), [(2, 0), (0, 1)], 'p', 'q'),
               (('Modus Ponens', ['a', 'a -> b'], 'b'), [(2, 0), (1, 1)], 'p', 'r'),
               (('Conjunction', ['a', 'b'], 'a & b'), [(2, 0), (2, 0)], 'p', 'p')]
        self.assertEqual(applic, exp)

    def test_modus_tollens_rule(self):
        args = ["~p", "q -> p"]
        claim = "~q"
        state = sh.pack(args, claim, [])
        applic = rh.applicable_rules(state)
        exp = [(('Modus Tollens', ['~b', 'a -> b'], '~a'), [(0, 0), (1, 1)], 'q', 'p')]
        self.assertEqual(applic, exp)


class QueueSearchTestCase(ut.TestCase):

    def test_solve_implication_bfs(self):
        args = ["p -> (q -> r)", "p", "q"]
        final_args = ["p -> (q -> r)", "p", "q", "q -> r", "r"]
        claim = "r"
        final_hist = [('Modus Ponens', (1, 0), 3), ('Modus Ponens', (2, 3), 4)]
        state = sh.initial_state(args, claim)
        problem = qs.SearchProblem(state, sh.proof_complete)
        plan, node_count = qs.breadth_first_search(problem)
        states = [problem.initial_state]
        for a in range(len(plan)):
            states.append(sh.apply_rule(plan[a], states[-1]))
        final_state = states[len(states)-1]
        (args, claim, hist) = sh.unpack(final_state)
        self.assertEqual(args, final_args)
        self.assertEqual(hist, final_hist)

    def test_solve_conjunction_bfs(self):
        args = ["p -> q", "s -> r", "p", "s"]
        final_args = ["p -> q", "s -> r", "p", "s", "q", "r", "r & q"]
        claim = "r & q"
        final_hist = [('Modus Ponens', (2, 0), 4),
                      ('Modus Ponens', (3, 1), 5),
                      ('Conjunction', (5, 4), 6)]
        state = sh.initial_state(args, claim)
        problem = qs.SearchProblem(state, sh.proof_complete)
        plan, node_count = qs.breadth_first_search(problem)
        states = [problem.initial_state]
        for a in range(len(plan)):
            states.append(sh.apply_rule(plan[a], states[-1]))
        final_state = states[len(states)-1]
        (args, claim, hist) = sh.unpack(final_state)
        self.assertEqual(args, final_args)
        self.assertEqual(hist, final_hist)

    def test_solve_mult_implication_bfs(self):
        args = ["p -> q", "p -> r", "p"]
        final_args = ["p -> q", "p -> r", "p", "q", "r", "r & q"]
        claim = "r & q"
        final_hist = [('Modus Ponens', (2, 0), 3),
                      ('Modus Ponens', (2, 1), 4),
                      ('Conjunction', (4, 3), 5)]
        state = sh.initial_state(args, claim)
        problem = qs.SearchProblem(state, sh.proof_complete)
        plan, node_count = qs.breadth_first_search(problem)
        states = [problem.initial_state]
        for a in range(len(plan)):
            states.append(sh.apply_rule(plan[a], states[-1]))
        final_state = states[len(states)-1]
        (args, claim, hist) = sh.unpack(final_state)
        self.assertEqual(args, final_args)
        self.assertEqual(hist, final_hist)

    def test_solve_modus_tollens_bfs(self):
        args = ["p -> q", "q -> r", "~r"]
        final_args = ['p -> q', 'q -> r', '~r', '~q', '~p']
        claim = "~p"
        final_hist = [('Modus Tollens', (2, 1), 3), 
                      ('Modus Tollens', (3, 0), 4)]
        state = sh.initial_state(args, claim)
        problem = qs.SearchProblem(state, sh.proof_complete)
        plan, node_count = qs.breadth_first_search(problem)
        states = [problem.initial_state]
        for a in range(len(plan)):
            states.append(sh.apply_rule(plan[a], states[-1]))
        final_state = states[len(states)-1]
        (args, claim, hist) = sh.unpack(final_state)
        self.assertEqual(args, final_args)
        self.assertEqual(hist, final_hist)

    def test_solve_hypothetical_syllogism_bfs(self):
        args = ["p -> q", "q -> r", "r -> s"]
        final_args = ['p -> q', 'q -> r', 'r -> s', 'p -> r', 'p -> s']
        claim = "p -> s"
        final_hist = [('Hypothetical Syllogism', (0, 1), 3),
                      ('Hypothetical Syllogism', (3, 2), 4)]
        state = sh.initial_state(args, claim)
        problem = qs.SearchProblem(state, sh.proof_complete)
        plan, node_count = qs.breadth_first_search(problem)
        states = [problem.initial_state]
        for a in range(len(plan)):
            states.append(sh.apply_rule(plan[a], states[-1]))
        final_state = states[len(states)-1]
        (args, claim, hist) = sh.unpack(final_state)
        self.assertEqual(args, final_args)
        self.assertEqual(hist, final_hist)

    def test_solve_disjunctive_bfs(self):
        args = ["p -> (q | r)", "p", "~r"]
        final_args = ['p -> (q | r)', 'p', '~r', 'q | r', 'q']
        claim = "q"
        final_hist = [('Modus Ponens', (1, 0), 3), 
                      ('Disjunctive Syllogism', (3, 2), 4)]
        state = sh.initial_state(args, claim)
        problem = qs.SearchProblem(state, sh.proof_complete)
        plan, node_count = qs.a_star_search(problem, astar.simple_heuristic)
        states = [problem.initial_state]
        for a in range(len(plan)):
            states.append(sh.apply_rule(plan[a], states[-1]))
        final_state = states[len(states)-1]
        (args, claim, hist) = sh.unpack(final_state)
        self.assertEqual(args, final_args)
        self.assertEqual(hist, final_hist)

    def test_solve_implication_astar(self):
        args = ["p -> (q -> r)", "p", "q"]
        final_args = ["p -> (q -> r)", "p", "q", "q -> r", "r"]
        claim = "r"
        final_hist = [('Modus Ponens', (1, 0), 3), ('Modus Ponens', (2, 3), 4)]
        state = sh.initial_state(args, claim)
        problem = qs.SearchProblem(state, sh.proof_complete)
        plan, node_count = qs.a_star_search(problem, astar.simple_heuristic)
        states = [problem.initial_state]
        for a in range(len(plan)):
            states.append(sh.apply_rule(plan[a], states[-1]))
        final_state = states[len(states)-1]
        (args, claim, hist) = sh.unpack(final_state)
        self.assertEqual(args, final_args)
        self.assertEqual(hist, final_hist)


# Note that __main__ is written based on test function implementation
# from the following source.
#   Title:          roomba_heuristic_test.py
#   Author:         Garrett Katz
#   Availability:   CIS 667, Homework 01
if __name__ == "__main__":

    num, errs, fails = 0, 0, 0
    test_cases = [HelperTestCase, RuleTestCase, RuleDictTestCase, QueueSearchTestCase]
    
    for test_case in test_cases:
        test_suite = ut.TestLoader().loadTestsFromTestCase(test_case)
        res = ut.TextTestRunner(verbosity=2).run(test_suite)
        num += res.testsRun
        errs += len(res.errors)
        fails += len(res.failures)
    
    print("\nscore: %d of %d (%d errors, %d failures)" % (num - (errs+fails), num, errs, fails))