import virtualCell

solution = virtualCell.Solution(10000.0)
solution.setMetabolites()
solution.addCell(1000.0)

DNA = 'BB BBBABBBA AA BBAA BBBAADAADADDAA'

cell = solution.cells[-1]
cell.setMetabolites()
cell.addDNA(DNA)

print "\n-Proteins-"
cell.output('proteins')