import cell

solution = cell.Solution(24000.0)
solution.metabolites['AB'].amount = 2400.0

solution.addCell(1000.0)
solution.cells[0].metabolites['AB'].amount = 0.0

solution.cells[0].addProtein('transporter-AB', 10.0)
solution.cells[0].addProtein('transporter-A', 10.0)
solution.cells[0].addProtein('enzyme-ABase', 20.0)

solution.cells[0].output()
solution.output()

for t in range(1000):
    for cell in solution.cells:
        cell.update()

solution.cells[0].output()
solution.output()
