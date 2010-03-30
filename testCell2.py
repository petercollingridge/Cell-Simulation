import virtualCell
import graphDrawer

defaultMetabolites = virtualCell.defaultMetabolites
defaultMetabolites['FK'] = 1.6 / 10.0
defaultMetabolites['IL'] = 0.8 / 10.0
defaultMetabolites['FG'] = 0.6 / 10.0
defaultMetabolites['JG'] = 0.4 / 10.0

# Initilise Solution
solution = virtualCell.Solution(1000000.0)
solution.volume /= 64
solution.setMetabolites(defaultMetabolites)

DNA = 'BACC-BACD-BABCBBAD-BAACBBBA-BAABBCAA-BCAC-BCAD-BCAABDBB'.replace('-', 'DDAA')

def addCell(seq):
    solution.addCell(1000.0)
    solution.cells[-1].setMetabolites('default')
    solution.cells[-1].DNA = seq
    solution.cells[-1].interpretDNA()
    solution.cells[-1].outputProteins()

#addCell(DNA_sequences['Gen 70'])
addCell(DNA)

# Initilise Graph
graph = graphDrawer.Graph()
graphSeries = { 'E 1': solution.cells[0].metabolites['E'],
                'L 1': solution.cells[0].metabolites['L'],
                'H 1': solution.cells[0].metabolites['H'],
                'EL 1': solution.cells[0].metabolites['EL']}
solutionConcs = {'E (out)': solution.metabolites['E'],
                 'L (out)': solution.metabolites['L'],
                 'H (out)': solution.metabolites['H'],
                 'EL (out)': solution.metabolites['EL']}

series = graphSeries.keys()
series.sort()
for s in series:
    graph.addSeries(s)

# Run Simulation
for t in range(48000):
    for s in series:
        graph.addDataToSeries(s, 100*graphSeries[s].amount/graphSeries[s].volume)

    for cell in solution.cells:
        cell.update()

print "\n-Solution-"
solution.output()

for cell in solution.cells:
    print "\n-Cell-"
    cell.output()

#graph.outputSeries('top cell', series)
