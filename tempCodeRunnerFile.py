final_state = states[len(states)-1]
    print(final_state)
    (args, claim, hist) = sh.unpack(final_state)
    start_rule = hist[0][2]
    hist_index = 0
    for i in len(args):
        rule = "Assumption"
        if i >= start_rule:
            rule = hist[hist_index][2]
            rule += " "
            rule += hist[hist_index][1]
            hist_index += 1
        print(str(i+1) + ". " + args[i] + "     " + rule +"\n")