import cell

solution = cell.Solution(24000.0)
solution.metabolites['AB'].amount = 1000.0
solution.addCell(1000.0)

solution.cells[0].addProtein('transporter-AB', 10.0)
solution.cells[0].metabolites['AB'].amount = 10.0

for cell in solution.cells:
    cell.update()

solution.cells[0].output()
