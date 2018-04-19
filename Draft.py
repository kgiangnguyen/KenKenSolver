import itertools

combinations = itertools.combinations_with_replacement([1,2,3,4,5], 3)

for comb in combinations:
    print(comb)