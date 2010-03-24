import virtualCell
import graphDrawer

# Initilise Solution
solution = virtualCell.Solution(1000000.0)
solution.addDefaultMetabolites()
solution.metabolites['EL'].amount = solution.volume * 0.08
solution.metabolites['FK'].amount = solution.volume * 0.04

# Initilise Cell
solution.addCell(1000.0)
solution.cells[0].addDefaultMetabolites()
solution.cells[0].DNA = 'BACBDDAABACBDDAABAAADDAABAADDDAABCABDDAABABDBCAA'
solution.cells[0].DNA = 'BACBDDAABACBDDAABAADDDAABCABDDAABABDBCAA'      # No E transporter
solution.cells[0].DNA = 'BACBDDAABACBDDAABAAABBADDDAABCABDDAABABDBCAA'  # E - H antiporter
solution.cells[0].interpretDNA()
solution.cells[0].outputProteins()

# Initilise Graph
graph = graphDrawer.Graph()
graphSeries = { 'E (in)': solution.cells[0].metabolites['E'],
                'F (in)': solution.cells[0].metabolites['F'],
                'G (in)': solution.cells[0].metabolites['G'],
                'H (in)': solution.cells[0].metabolites['H'],
                'I (in)': solution.cells[0].metabolites['I'],
                'J (in)': solution.cells[0].metabolites['J'],}

series = graphSeries.keys()
series.sort()
for s in series:
    graph.addSeries(s)

#print "\n-Cell-"
#solution.cells[0].output()

# Run Simulation
for t in range(100000):
   # for s in series:
   #     graph.addDataToSeries(s, 100*graphSeries[s].amount/graphSeries[s].volume)

    for cell in solution.cells:
        cell.update()

#print "\n-Solution-"
#solution.output()

print "\n-Cell-"
solution.cells[0].output()

#graph.outputSeries('test', series)
