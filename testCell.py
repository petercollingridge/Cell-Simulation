import virtualCell
import drawSVGGraph

# Initilise Solution
solution_metabolites = virtualCell.default_metabolites
solution_metabolites['FK'] = 0.16
solution_metabolites['IL'] = 0.08
solution_metabolites['FG'] = 0.06
solution_metabolites['JG'] = 0.04
solution_metabolites['EL'] = 0.01
solution = virtualCell.Solution(24000.0, solution_metabolites)
#solution.output('metabolites')

# Initilise Cell
cell = solution.addCell(volume=1000.0, metabolites='default')
cell.metabolites['EH'].amount += 40     # Add ATP
cell.metabolites['F'].amount  += 20     # Add ATP
#cell.metabolites['JG'].amount += 40     # Add Amino acids

DNA  = 'AAAAAD BB AA BBBBBBBA AA BA ACAA DDAAAA'    # Transcription factor
DNA += 'AADAAD AA ACADAA DDAAAA'                    # FG pore
DNA += 'AADAAD AA ACBDAA DDAAAA'                    # FK pore
DNA += 'AADAAD AA BCADAA DDAAAA'                    # JG pore
DNA += 'AADAAD AA ADAA AB BBAA DDAAAA'              # G/I antiporter
DNA += 'AADAAD AA BAAA AB BDAA DDAAAA'              # H/K antiporter
DNA += 'AADAAD AC AC DDAAAA'                        # FGase
DNA += 'AADAAD AC AD DDAAAA'                        # FKase
DNA += 'AADAAD AA ACAA AC AA DDAAAA'                # F-driven EHase

cell.addDNA(DNA)

for seq in cell.proteins:
    cell.proteins[seq].amount += 1
cell.output('metabolites')
cell.proteins['LNLNL'].amount += 1

# Data recording options
data_collection_functions = {\
    '[JG]': (lambda cell: cell.metabolites['JG'].amount),
    '[EH]': (lambda cell: cell.metabolites['EH'].amount),
    '[tf]': (lambda cell: 10*cell.proteins['QLQQQPLPNL'].amount)}
   #'tf on tf': (lambda cell: cell.proteins['QLQPQPLPNL'].binding_domains[0].targets[cell.genes[0]][1])}
data_collection = dict([(key, []) for key in data_collection_functions.keys()])

# Run Simulation
run_time = 50000
for t in range(run_time):
    #cell.metabolites['EH'].amount = 80  # Keep ATP constant
    #cell.metabolites['JG'].amount = 40  # Keep amino acids constant
    solution.update()
    
    for d in data_collection.keys():
        data_collection[d].append(data_collection_functions[d](cell))

# Output
print "\n\t-Solution-\t-Cell-"
metabolites = solution.metabolites.keys()
metabolites.sort()

for m in metabolites:
    print '%s\t%.3f%%\t\t%2.3f%%' % (m, solution.metabolites[m].concentration(), cell.metabolites[m].concentration())

cell.output('proteins')

g = drawSVGGraph.Graph()
g.x_axis_label = "Time"
g.y_axis_label = "Concentration"
g.data = data_collection

g.outputSVG('tf graph', width=400, height=250)