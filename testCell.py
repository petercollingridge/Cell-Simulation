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
solution.output('metabolites')

# Initilise Cell
DNA = 'BACBCBCCDBB DDAA DBCCAABCABACCDCBDCBDDCA DDAA DADBABBABDBCAACDD DDAA BABDBBAD DDAA BABDBBADDDAADADBABBABDBCAACDDDDAABABDBBADAD'
DNA = 'CABCAA-CABCAA-BACC-BACD-BADD-BAADBBBC-BAACBBBA-BCAC-BCAD-BAABBCAA-BCAABDBB'.replace('-', 'DDAA')
DNA = 'CBBABAAA-BAAA-BAAD-BACB-BACB-BCAB-BCAABABD'.replace('-', 'DDAA')

solution.addCell(1000.0)
cell = solution.cells[-1]
cell.setMetabolites('default')
cell.addDNA(DNA)

for seq in cell.genes:
    cell.proteins[seq].amount += 1

print "\n-Proteins-"   
cell.output('proteins')    

# Run Simulation
solution.update(2000)

# Output
print "\t-Solution-\t-Cell-"
metabolites = solution.metabolites.keys()
metabolites.sort()

v1, v2 = solution.volume, cell.volume
#for m in metabolites:
#    print '%s\t%.3f%%\t\t%2.3f%%' % (m, 100*solution.metabolites[m].amount/v1, 100*solution.cells[-1].metabolites[m].amount/v2)

print "\n-Proteins-"   
#cell.output('proteins')    