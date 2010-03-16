import biochemistry

solution = biochemistry.Solution(8000.0)
solution.metabolites['ATP'] = 1000.0
solution.addCell(1000.0)

solution.cells[0].addProtein('transporter-ATP', 10.0)
solution.cells[0].metabolites['ATP'] = 10.0

for cell in solution.cells:
    cell.update()

def output():
    for m in biochemistry.all_metabolites:
        print "%s\t%s\t%s" %(m, solution.metabolites[m], cell.metabolites[m])

    for p in cell.proteins.values():
        print p.sequence

output()
