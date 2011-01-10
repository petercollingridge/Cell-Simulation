import virtualCell

solutionMetabolites = virtualCell.default_metabolites
solutionMetabolites['FK'] = 1.6 / 10.0
solutionMetabolites['IL'] = 0.8 / 10.0
solutionMetabolites['FG'] = 0.6 / 10.0
solutionMetabolites['JG'] = 0.4 / 10.0
solutionMetabolites['EL'] = 0.1 / 10.0

# Initilise Solution
solution = virtualCell.Solution(1000000.0/64)
solution.setMetabolites(solutionMetabolites)

# Initilise Cell
DNA = 'CABCAA-CABCAA-BACC-BACD-BADD-BAADBBBC-BAACBBBA-BCAC-BCAD-BAABBCAA-BCAABDBB'.replace('-', 'DDAA')
solution.addCell(1000.0)
solution.cells[-1].setMetabolites('default')
solution.cells[-1].addDNA(DNA)

for p in solution.cells[-1].proteins.values():
    p.amount = 1

print "\n-Proteins-"   
solution.cells[-1].output('proteins')    

# Run Simulation
solution.update(48000)

# Output
print "\n-Solution-"
solution.output('metabolites')
print "\n-Cell-"
solution.cells[-1].output('metabolites')
