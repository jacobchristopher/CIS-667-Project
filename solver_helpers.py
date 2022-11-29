import rule_helpers as rh

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
    return pack(arguments, claim, [])


# Check if the goal state has been reached
def proof_complete(state: tuple) -> bool:
    (args, claim, hist) = unpack(state)
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
    return rh.applicable_rules(state)


# Update the state by applying the given rule
def apply_rule(rule: tuple, state: tuple) -> tuple:
    (args, claim, hist) = unpack(state)
    (form, indices, a, b) = rule
    (name, pattern, concl) = form

    # Add to the hist element; tuple contains name of rule, indices that are 
    # referenced, and the index that the new arg will be added at
    # Note: Not storing index in rule in history (as it is sorted)
    # FIXME: Add this conversion to (and from) tuple into pack/unpack?
    hist.append((name, tuple(rh.take_1_of_2_mapper(indices)), len(args)))
    result = rh.convert_to_complex(concl, a, b)
    args.append(result)
    return pack(args, claim, hist)

#-------------------------------------------------------------------------

# Packs the state into a hashable object
def pack(args, claim, hist):
        return (tuple(args), claim, tuple(hist))

# Unpacks the state into a mutable object
def unpack(state):
    args, claim, hist = state
    return list(args), claim, list(hist)
