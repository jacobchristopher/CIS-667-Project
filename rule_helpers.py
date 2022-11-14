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
    simplified = "a " + term + " b"
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