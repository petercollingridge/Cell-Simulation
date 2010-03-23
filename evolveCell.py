import cell
import graphDrawer

solution = cell.Solution(1000000.0)
solution.addDefaultMetabolites()
solution.metabolites['EL'].amount = solution.volume * 0.08
solution.metabolites['FK'].amount = solution.volume * 0.04

solution.addCell(1000.0)
solution.cells[0].addDefaultMetabolites()

solution.cells[0].DNA = 'BACBDDAABACBDDAABAAADDAABAADDDAABCABDDAABABDBCAA'
solution.cells[0].interpretDNA()

for t in range(10000):
    for cell in solution.cells:
        cell.update()

#print "\n-Solution-"
#solution.output()

print "\n-Cell-"
solution.cells[0].output()


