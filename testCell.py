import biochemistry

solution = biochemistry.Solution(8.0)
solution.metabolites['ATP'] = 1000.0
solution.addCell(1.0)

solution.cells[0].addProtein('transporter-ATP', 10.0)
solution.cells[0].metabolites['ATP'] = 10.0

for cell in solution.cells:
    cell.update()

for m in solution.metabolites.keys():
    print m, solution.metabolites[m]

for p in cell.proteins.values():
    print p.sequence
