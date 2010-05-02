import timeit

t = timeit.Timer('x = virtualCell.Solution(1000) \nx.setMetabolites("default")', 'import virtualCell')

test_result = t.repeat(3, 100000)
print min(test_result)