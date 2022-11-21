import solver_helpers as sh

# This file will contain helper functions for finding which inference rules
# are applicable in a given state.

# Parse into tuple containing
#   1. The simplified expression
#   2. The original terms in the expression
def parse_expression(exp: str) -> tuple:  
    # TODO: Check for negation

    # Check if first term is paren
    astart = 0
    aend = 1
    if exp[astart:aend] == "(":
        aend = find_end_paren(exp, astart)
    a = exp[astart:aend]

    tstart = aend+1
    term = exp[tstart:tstart+1]
    if term == "-":
        term = "->"
        tstart += 1
    tend = tstart+1

    bstart = tend+1
    bend = bstart+1
    if exp[bstart:bend] == "(":
        bend = find_end_paren(exp, bstart)
    b = exp[bstart:bend]
    simplified = ""
    if len(a) > 0:
        simplified += "a"
    if len(term) > 0:
        simplified += " " + term + " b"
    return (simplified, a, b)


# Find the closing parenthesis for the open parenthesis at the given index
# with the string exp
def find_end_paren(exp: str, index: int) -> int:
    substr = exp[index:]
    count = 1
    i = 1
    while count > 0:
        s = substr[i:i+1]
        if s == '(':
            count += 1
        elif s == ')':
            count -=1
        i += 1
    return i+index

# Reconstruct complex expression
def convert_to_complex(expr: str, a: str, b:str) -> str:
    new_expr = expr.replace("a", a)
    new_expr = new_expr.replace("b", b)
    return new_expr

def get_ab_vars(rule, args) -> tuple:
    return("a", "b") #TODO: implement

#--------------------------------------------------------------

#TODO: rectify differences between solver_helper def and this one
rule_dict = [("Modus Ponens", ["a", "a -> b"], "b")]

# Find applicable rules from the rule dictionary
def applicable_rules(state: tuple) -> list:
    (args, claim, hist) = sh.unpack(state)
    can_apply = []
    for rules in rule_dict:
        cond_index = [] # a list to contain all args that match the rule
        (name, rule_args, cond) = rules
        i = 0
        b = ""
        for arg in args:
            (simp, new_a, new_b) = parse_expression(arg)

            # FIXME: This should not be necessary when TODO below is 
            # implemented (final 'a' and 'b' values sourced from there)
            a = new_a
            if not new_b == "":
                b = new_b
            
            if simp in rule_args:
                # Form is:
                # 1. Index in args
                # 2. Index in rule
                # 3. 'a'
                # 4. 'b'
                cond_index.append((i, rule_args.index(simp), a, b))
            i += 1
        cond_index.sort(key = lambda x: x[1])
        # TODO: Check for common "a" and "b" variables to see if any
        #       multiple arg rules can be applied
        #       Then, drop 'a' and 'b' values from tuple.
        cond_index = take_2_of_4_mapper(cond_index)
        arg_pairings = cond_index #FIXME
        can_apply.append((rules, arg_pairings, a, b))
    return can_apply


def take_2_of_4_mapper(lst: list) -> list:
    rtrn_lst = []
    for i in range(len(lst)):
        (one, two, three, four) = lst[i]
        rtrn_lst.append((one, two))
    return rtrn_lst

def take_1_of_2_mapper(lst: list) -> list:
    rtrn_lst = []
    for i in range(len(lst)):
        (one, two) = lst[i]
        rtrn_lst.append(one)
    return rtrn_lst