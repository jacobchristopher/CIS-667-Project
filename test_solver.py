import unittest as ut
import solver_helpers as sh
import rule_helpers as rh

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
        exp = [(('Modus Ponens',['a', 'a -> b'], 'b'), [(1, 0), (0, 1)], 'p', 'q')]
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

    def test_applicable_rules1(self):
        args = ["p -> q", "p"]
        claim = "q"
        state = sh.pack(args, claim, [])
        applic = rh.applicable_rules(state)
        exp = [(('Modus Ponens', ['a', 'a -> b'], 'b'), [(1, 0), (0, 1)], 'p', 'q')]
        self.assertEqual(applic, exp)

    def test_applicable_rules2(self):
        args = ["p -> q", "p", "x -> y", "x"]
        claim = "q"
        state = sh.pack(args, claim, [])
        applic = rh.applicable_rules(state)
        exp = [(('Modus Ponens', ['a', 'a -> b'], 'b'), [(1, 0), (0, 1)], 'p', 'q'), 
               (('Modus Ponens', ['a', 'a -> b'], 'b'), [(3, 0), (2, 1)], 'x', 'y')]
        self.assertEqual(applic, exp)


# Note that __main__ is written based on test function implementation
# from the following source.
#   Title:          roomba_heuristic_test.py
#   Author:         Garrett Katz
#   Availability:   CIS 667, Homework 01
if __name__ == "__main__":

    num, errs, fails = 0, 0, 0
    test_cases = [HelperTestCase, RuleTestCase]
    
    for test_case in test_cases:
        test_suite = ut.TestLoader().loadTestsFromTestCase(test_case)
        res = ut.TextTestRunner(verbosity=2).run(test_suite)
        num += res.testsRun
        errs += len(res.errors)
        fails += len(res.failures)
    
    print("\nscore: %d of %d (%d errors, %d failures)" % (num - (errs+fails), num, errs, fails))