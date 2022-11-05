# The state of the problem will be represented by a tuple with three elements:
#
# - args:   A list containing initial assumptions and expressions that have
#           been proven. 
#
# - claim:  This will represent the goal state that needs to be proven.
#           Inference rules will continue to be applied until claim is an
#           element of the arguments list.
#
# - hist:   A list of inference rules that have been applied to get to the 
#           current state. This will be referenced for the final output of
#           the proof.

# Create the intial state tuple based on the argument and claim input
def initial_state(arguments: list, claim: str) -> tuple:
    return (arguments, claim, [])


# Check if the goal state has been reached
def proof_complete(state: tuple) -> bool:
    (args, claim, hist) = state
    return claim in args


# Return list of valid actions in the current state with the following form:
#
# - name:   The str name of the rule to be applied; this will be added to
#           the hist list in state.
#
# - form:   Pattern matching for the format of the inference rule.
#
# - index:  A list of the indices of the element of args that this rule 
#           applies to.
def valid_actions(state: tuple) -> list:
    # TODO: Implement pattern matching to check what rules
    #       can be applied to the current list of args
    # TODO: Create dictionary of inference rules that
    #       will be referenced here
    return None


# Update the state by applying the given rule
def apply_rule(rule: tuple, state: tuple) -> tuple:
    (args, claim, hist) = state
    (name, form, index) = rule

    # Add to the hist element; tuple contains name of rule, indices that are 
    # referenced, and the index that the new arg will be added at
    hist.append((name, index, args.length))

    result = None       # TODO: Add logic to apply a given rule using form
    args.append(result)
    return (args, claim, hist)
