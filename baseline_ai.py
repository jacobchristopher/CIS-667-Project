import random
import solver_helpers as sh
import rule_helpers as rh

# A baseline AI that applies random actions
# Return:
#   - Final state
#   - If proof is complete
#   - Number of steps taken
def apply_random_actions(state, count = 100):
    steps = 0
    for a in range(count):
        applic_rules = sh.valid_actions(state)
        to_apply = random.choice(applic_rules)
        state = sh.apply_rule(to_apply, state)
        steps += 1
        if sh.proof_complete(state):
            break
    return (state, sh.proof_complete(state), steps)