import solver_helpers as sh

# This file will contain helper functions for finding which inference rules
# are applicable in a given state.

# Parse into tuple containing
#   1. The simplified expression
#   2. The original terms in the expression
def parse_expression(exp: str) -> tuple: 
    # 'a' 
    astart = 0
    aend = 1
    negation_a = False
    # Check for negation
    if exp[astart:aend] == "~":
        negation_a = True
        astart += 1
        aend += 1
    # Parse expression a
    if exp[(aend-1):aend] == "(":
        aend = find_end_paren(exp, astart)
    a = exp[astart:aend]
    # Term
    tstart = aend+1
    term = exp[tstart:tstart+1]
    # Parse operator (if exists)
    if term == "-":
        term = "->"
        tstart += 1
    tend = tstart+1
    # 'b'
    bstart = tend+1
    bend = bstart+1
    negation_b = False
    # Check for negation
    if exp[bstart:bend] == "~":
        negation_b = True
        bstart += 1
        bend += 1
    # Parse expression b
    if exp[bstart:bend] == "(":
        bend = find_end_paren(exp, bstart)
    b = exp[bstart:bend]
    # Format into output
    simplified = ""
    if negation_a:
        simplified += "~"
    if len(a) > 0:
        simplified += "a"
    if len(term) > 0:
        simplified += " " + term + " " 
    if negation_b:
        simplified += "~"
    if len(b) > 0:
        simplified += "b"
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

#--------------------------------------------------------------

# Dictionary of currently implemented inference rules
rule_dict = [("Modus Ponens", ["a", "a -> b"], "b"), 
             ("Modus Tollens", ["~b", "a -> b"], "~a"),
             ("Simplification", ["a & b"], "a"),
             ("Simplification", ["a & b"], "b"),
             ("Conjunction", ["a", "b"], "a & b"),
             ("Disjunctive Syllogism", ["a | b", "~a"], "b"),
             ("Disjunctive Syllogism", ["a | b", "~b"], "a"),
             ("Hypothetical Syllogism", ["a -> b"], "a -> b")]

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
            (simp, a, b) = parse_expression(arg)
            if simp in rule_args:
                rule_idx = rule_args.index(simp)
                # Form is:
                # 1. Index in args
                # 2. Index in rule
                # 3. 'a'
                # 4. 'b'
                cond_index.append((i, rule_idx, a, b))
            elif simp.replace('a', 'b') in rule_args:
                simp = simp.replace('a', 'b')
                rule_idx = rule_args.index(simp)
                b = a
                a = ""
                cond_index.append((i, rule_idx, a, b))
            i += 1
        cond_index.sort(key = lambda x: x[1])
        arg_pairings = find_common_pairings(rules, cond_index)
        can_apply.extend(arg_pairings)
    return can_apply

# A helper method for applicable_rules()
def find_common_pairings(rules: tuple, cond_index: list) -> list:
    (name, rule_args, cond) = rules
    if name == "Conjunction": return conjuntion_pairs(cond_index, rules)                            # Special Case #1
    elif name == "Modus Ponens": return modus_ponens_pairs(cond_index, rules)                       # Special Case #2
    elif name == "Modus Tollens": return modus_tollens_pairs(cond_index, rules)                     # Special Case #3
    elif name == "Hypothetical Syllogism": return hypothetical_syllogism_pairs(cond_index, rules)   # Special Case #4
    else: return standard_pairs(cond_index, rules)                                                  # Standard Case

# ---------------------------------------------------------------

# Groups conditions for conjungation rule
def conjuntion_pairs(cond_index: list, rules: tuple) -> list:
    pairing_list = []
    for x in cond_index:
        a = x[2]
        for y in cond_index:
            b = y[2]
            if len(a) != 1:
                a = "(" + unwrapped(a) + ")"
            if len(b) != 1:
                "(" + unwrapped(b) + ")"
            elem = (rules, take_2_of_4_mapper([x,y]), a, b)
            if elem not in pairing_list:
                pairing_list.append(elem)
    return pairing_list

# Groups conditions for modus ponens rule
def modus_ponens_pairs(cond_index: list, rules: tuple) -> list:
    (name, rule_args, cond) = rules
    pairing_list = []
    rule_a = []
    for x in cond_index:
        if x[3] == "":
            rule_a.append(x)
    for x in cond_index:
        a = x[2]
        b = x[3]
        for y in rule_a:
            if y[2] == a and b != "":
                pairing_list.append((y, x))
    return pairing_list_parser(pairing_list, rules)

# Groups conditions for modus ponens rule
def modus_tollens_pairs(cond_index: list, rules: tuple) -> list:
    (name, rule_args, cond) = rules
    pairing_list = []
    rule_a = []
    for x in cond_index:
        if x[2] == "":
            rule_a.append(x)
    for x in cond_index:
        a = x[2]
        b = x[3]
        for y in rule_a:
            if y[3] == b and a != "":
                pairing_list.append((y, x))
    return pairing_list_parser(pairing_list, rules)

# Groups conditions for hypothetical syllogism rule
def hypothetical_syllogism_pairs(cond_index: list, rules: tuple) -> list:
    (name, rule_args, cond) = rules
    pairing_list = []
    rule_a = []
    for x in cond_index:
        for y in cond_index:
            a = x[2]
            b = y[3]
            if y[2] == x[3]:
                elem = (rules, take_2_of_4_mapper([x,y]), a, b)
                if elem not in pairing_list:
                    pairing_list.append(elem)
    return pairing_list

# Catch all condition grouper for those without a special definition
def standard_pairs(cond_index: list, rules: tuple) -> list:
    (name, rule_args, cond) = rules
    pairing_list = []
    for x in cond_index:
        common_rules = []
        a = x[2]
        b = x[3]
        for y in cond_index:
            if y[2] == a or y[2] == "":
                if y[3] == b or b == "":
                    if y not in common_rules: common_rules.append(y)
        pairing_list.append(tuple(common_rules))
    return pairing_list_parser(pairing_list, rules)

# Formatter for condition groupers
def pairing_list_parser(pairing_list: list, rules: tuple) -> list:
    (name, rule_args, cond) = rules
    final_list = []
    for x in pairing_list:
        if len(x) == len(rule_args):
            a = x[0][2]
            b = x[0][3]
            index = 1
            while a == "":
                if index < (len(x)):
                    a = x[index][2]
                    index += 1
                else:
                    break
            index = 1
            while b == "":
                if index < (len(x)):
                    b = x[index][3]
                    index += 1
                else:
                    break
            elem = (rules, take_2_of_4_mapper(list(x)), unwrapped(a), unwrapped(b))
            if elem not in final_list:
                final_list.append(elem)
    return final_list

# ---------------------------------------------------------------

# Tuple parsing helper function
def take_2_of_4_mapper(lst: list) -> list:
    rtrn_lst = []
    for i in range(len(lst)):
        (one, two, three, four) = lst[i]
        rtrn_lst.append((one, two))
    return rtrn_lst

# Tuple parsing helper function
def take_1_of_2_mapper(lst: list) -> list:
    rtrn_lst = []
    for i in range(len(lst)):
        (one, two) = lst[i]
        rtrn_lst.append(one)
    return rtrn_lst

# Parenthesis parsing helper function
def unwrapped(exp: str) -> str:
    if exp[0:1] == "(":
        end = find_end_paren(exp, 0)
        if end == len(exp):
            return exp[1:end-1]
    return exp
