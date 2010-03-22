import cell
import graphDrawer

solution = cell.Solution(24000.0)
solution.addCell(1000.0)

solution.metabolites['AB'].amount = 2400.0

solution.cells[0].addProtein('transporter-AB', 10.0)
solution.cells[0].addProtein('transporter-A', 10.0)
solution.cells[0].addProtein('enzyme-ABase', 20.0)

graph = graphDrawer.Graph()
graphSeries = { 'A (in)':  solution.cells[0].metabolites['A'],
                'B (in)':  solution.cells[0].metabolites['B'],
                'AB (in)': solution.cells[0].metabolites['AB'],
                'A (out)': solution.metabolites['A'],
                'B (out)': solution.metabolites['B'],
                'AB (out)': solution.metabolites['AB']}

series = graphSeries.keys()
series.sort()
for s in series:
    graph.addSeries(s)

for t in range(300):
    for s in series:
        graph.addDataToSeries(s, 100*graphSeries[s].amount/graphSeries[s].volume)

    for cell in solution.cells:
        cell.update()

solution.cells[0].output()
solution.output()

graph.outputSeries('test', series)
