import virtualCell
import graphDrawer

# Initilise Solution
solution = virtualCell.Solution(1000000.0)
solution.volume /= 16
solution.addDefaultMetabolites()
solution.metabolites['EL'].amount = solution.volume * 0.08
solution.metabolites['FK'].amount = solution.volume * 0.04

DNA = {'Ancestor' : 'BACBDDAABACBDDAABAAADDAABAADDDAABCABDDAABABDBCAA',
       'No E pore': 'BACBDDAABACBDDAABAADDDAABCABDDAABABDBCAA',
       'E/H antiporter' : 'BACBDDAABACBDDAABAAABBADDDAABCABDDAABABDBCAA',
       'Gen 1': 'BACBDDAABACBDDAABAAADDAABAADDDAABCABDDAABABDBCAADADADBDDCBACCCCAACC',
       'Gen 2800': 'BACBCCDBCBCAADADDAABABDBBADDCCAAADADBACCBCADCCDDAABCABDDAABABDBCAACCACACABDCAADDAABABDBBADCBDDDAABACBCCDBCBCAADADDAABABDBBADDADDABADCABCBDDAABCABDDAABABDBCAADDCDCDDDDAABABDBBADBACDDAABACBCCDBCBCAADADDAABABDBBADDACDAADBAAAADDDAABCABDDAABABDBCAAAAACCDCABDDAABABDBCAAADDDDDABCCAACBADCDADDAABABDBBADCBCDDAABABDBBADDCDABBDDAABABDBCAAACACCDCCDCBAB',
       'Gen 2739': 'BACBCCDBCBCAADADDAABABDBBADDCCAAADACDACCBCADCCDDAABCABDDAABABDBCAACCCCACABDCAADDAABABDBBADCBDDDAABACBCCDBCBCAADADDAABABDBBADDADDABADCABCBDDAABCABDDAABABDBCAADDCDCDDBCAADDCDDDDAABABDBBADBACDDAABACBCCDBCBCAADADDAABABDBBADDACDAADBAAAADDDAABCABDDAABABDBCAADAACCDCABDDAABABDBCAAADDADDABCCAAABADCDADDAABABDBBADCBCDDADDAABABDBBADBACDDAABACBCCDBCBCAADADDAABABDBBADDACDAADBAAAADDDAABCABDDAABABDBCAADAACCDCABDDAABABDBCAAADDDDDABCCAACBADCDADDAABABDBBADCBCDDAABABDBBADDCDABBDDAABABDBCAAACACCDCCDCBAB',
'Gen2, 1263': 'BACBCBCCDBBDDAADBCCAABCABACCDCBDCBDDCADDAADADBABBABDBCAACDDDDAABABDBBADDDAABABDBBADDDAADADBABBABDBCAACDDDDAABABDBBADAD'}

def addCell(DNA_seq):
    solution.addCell(1000.0)
    solution.cells[-1].addDefaultMetabolites()
    solution.cells[-1].DNA = DNA[DNA_seq]
    solution.cells[-1].interpretDNA()
    solution.cells[-1].outputProteins()

addCell('Gen2, 1263')

# Initilise Graph
graph = graphDrawer.Graph()
graphSeries = { 'E 1': solution.cells[0].metabolites['E'],
                'L 1': solution.cells[0].metabolites['L'],
                'H 1': solution.cells[0].metabolites['H'],
                'EL 1': solution.cells[0].metabolites['EL']}
#graphSeries1 = {'E 2': solution.cells[1].metabolites['E'],
#                'L 2': solution.cells[1].metabolites['L'],
#                'H 2': solution.cells[1].metabolites['H'],
#                'EL 2': solution.cells[1].metabolites['EL']}
graphSeries2 = { 'E (out)': solution.metabolites['E'],
                'L (out)': solution.metabolites['L'],
                'H (out)': solution.metabolites['H'],
                'EL (out)': solution.metabolites['EL']}

series = graphSeries.keys()
series.sort()
for s in series:
    graph.addSeries(s)

# Run Simulation
for t in range(20000):
    for s in series:
        graph.addDataToSeries(s, 100*graphSeries[s].amount/graphSeries[s].volume)

    for cell in solution.cells:
        cell.update()

print "\n-Solution-"
solution.output()

for cell in solution.cells:
    print "\n-Cell-"
    cell.output()

graph.outputSeries('top cell', series)
