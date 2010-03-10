import biochemistry

solution = biochemistry.Solution(8.0)
solution.metabolites['ATP'] = 1000.0

cell = biochemistry.Cell(1.0)

for m in solution.metabolites.keys():
    print m, solution.metabolites[m]
