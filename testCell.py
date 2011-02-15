import virtualCell

# Initilise Solution
solution_metabolites = virtualCell.default_metabolites
solution_metabolites['FK'] = 0.16
solution_metabolites['IL'] = 0.08
solution_metabolites['FG'] = 0.06
solution_metabolites['JG'] = 0.04
solution_metabolites['EL'] = 0.01
solution = virtualCell.Solution(24000.0, solution_metabolites)

# Initilise Cell
DNA = 'BACBCBCCDBB DDAA DBCCAABCABACCDCBDCBDDCA DDAA DADBABBABDBCAACDD DDAA BABDBBAD DDAA BABDBBADDDAADADBABBABDBCAACDDDDAABABDBBADAD'
DNA = 'CABCAA-CABCAA-BACC-BACD-BADD-BAADBBBC-BAACBBBA-BCAC-BCAD-BAABBCAA-BCAABDBB'.replace('-', 'DDAA')
DNA = 'CBBABAAA-BAAA-BAAD-BACB-BACB-BCAB-BCAABABD'.replace('-', 'DDAA')
cell = solution.addCell(volume=1000.0, metabolites='default')
cell.addDNA(DNA)

for seq in cell.proteins:
    cell.proteins[seq].amount += 1
    cell.proteins[seq].degradation_rate = 0

solution.output('metabolites')
print "\n-Proteins-"   
cell.output('proteins')    

# Run Simulation
solution.update(2000)

# Output
print "\t-Solution-\t-Cell-"
metabolites = solution.metabolites.keys()
metabolites.sort()

for m in metabolites:
    print '%s\t%.3f%%\t\t%2.3f%%' % (m, solution.metabolites[m].concentration(), cell.metabolites[m].concentration())

print "\n-Proteins-"   
#cell.output('proteins')    