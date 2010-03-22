import cell
import graphDrawer

solution = cell.Solution(24000.0)
solution.addCell(1000.0)

solution.metabolites['AB'].amount = 2400.0
solution.cells[0].metabolites['C'].amount = 100.0
solution.cells[0].metabolites['D'].amount = 100.0
solution.cells[0].metabolites['CD'].amount = 100.0

solution.cells[0].addProtein('tra-AB', 10.0)
solution.cells[0].addProtein('rxn-f-ABase', 20.0)
solution.cells[0].addProtein('rxn-f-CDase-tra-A', 5.0)

graph = graphDrawer.Graph()
graphSeries = { 'A (in)':  solution.cells[0].metabolites['A'],
                'B (in)':  solution.cells[0].metabolites['B'],
                'AB (in)': solution.cells[0].metabolites['AB'],
                'C (in)':  solution.cells[0].metabolites['C'],
                'D (in)':  solution.cells[0].metabolites['D'],
                'CD (in)': solution.cells[0].metabolites['CD'],
                'A (out)': solution.metabolites['A'],
                'B (out)': solution.metabolites['B'],
                'AB (out)': solution.metabolites['AB']}

series = graphSeries.keys()
series.sort()
for s in series:
    graph.addSeries(s)

print "\n-Cell-"
solution.cells[0].output()

for t in range(20000):
   # for s in series:
   #     graph.addDataToSeries(s, 100*graphSeries[s].amount/graphSeries[s].volume)

    for cell in solution.cells:
        cell.update()

print "\n-Cell-"
solution.cells[0].output()
#solution.output()

#graph.outputSeries('test', series)
