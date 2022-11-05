import unittest as ut
import solver_helpers as sh

class HelperTestCase(ut.TestCase):

    def test_initial_state(self):
        args = ["p > q", "p"]
        claim = "q"
        state  = sh.initial_state(args, claim)
        expected_state = (args, claim, [])
        self.assertEqual(state, expected_state)

    def test_proof_complete(self):
        args = ["p > q", "p"]
        claim = "q"
        args.append(claim)
        state = (args, claim, [])
        self.assertTrue(sh.proof_complete(state))
    
    def test_proof_incomplete(self):
        args = ["p > q", "p"]
        claim = "q"
        state = (args, claim, [])
        self.assertFalse(sh.proof_complete(state))


# Please note that __main__ is written based on test function implementation
# from the following source.
#   Title:          roomba_heuristic_test.py
#   Author:         Garrett Katz
#   Availability:   CIS 667, Homework 01
if __name__ == "__main__":

    num, errs, fails = 0, 0, 0
    test_cases = [HelperTestCase]
    
    for test_case in test_cases:
        test_suite = ut.TestLoader().loadTestsFromTestCase(test_case)
        res = ut.TextTestRunner(verbosity=2).run(test_suite)
        num += res.testsRun
        errs += len(res.errors)
        fails += len(res.failures)
    
    print("score: %d of %d (%d errors, %d failures)" % (num - (errs+fails), num, errs, fails))