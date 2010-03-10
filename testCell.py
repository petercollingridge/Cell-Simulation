import biochemistry

solution = biochemistry.Solution(8.0)
solution.metabolites['ATP'] = 1000.0

cell = biochemistry.Cell(1.0)
cell.addProtein('transporter-ATP', 10.0)
cell.metabolites['ATP'] = 10.0
cell.update()

for m in solution.metabolites.keys():
    print m, solution.metabolites[m]

for p in cell.proteins.values():
    print p.sequence
