bools = [True,False]
for A in bools:
    for B in bools:
        for C in bools:
            original = not(((A and not B) or C) or ((A and C) and not B))
            final = not A and not C or B and not C
            intermediate = (not A or B) and not C and ((not A or not C or B))
            it = (not A or B) and not C
            test = not C
            print(original == final)