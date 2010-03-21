import cell
import graphDrawer

solution = cell.Solution(24000.0)
solution.addCell(1000.0)

solution.metabolites['AB'].amount = 2400.0

solution.cells[0].addProtein('transporter-AB', 10.0)
solution.cells[0].addProtein('transporter-A', 10.0)
solution.cells[0].addProtein('enzyme-ABase', 20.0)

graph = graphDrawer.Graph()
graphSeries = { 'Cell A': solution.cells[0].metabolites['A'],
                'Cell B': solution.cells[0].metabolites['B'],
                'Cell AB': solution.cells[0].metabolites['AB']}

for g in graphSeries.keys():
    graph.addSeries(g)

for t in range(1000):
    for g in graphSeries.keys():
        graph.addDataToSeries(g, graphSeries[g].amount)

    for cell in solution.cells:
        cell.update()

solution.cells[0].output()
solution.output()

for n in range(0, 1000, 10):
    print "%.2f\t%.2f\t%.2f" % (graph.series['Cell A'][n], graph.series['Cell B'][n], graph.series['Cell AB'][n])

graph.graphSeries(['Cell A', 'Cell B', 'Cell AB'])
