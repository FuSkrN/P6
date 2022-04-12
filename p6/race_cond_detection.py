def race_cond_check(stateArray):
    counter = 0
    for state in reversed(stateArray):
        if len(state.programCounters) == 0:
            counter = counter + 1
        else:
            break
    return counter
