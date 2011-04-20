import virtualCell
import drawSVGGraph

DNA  = 'AADADD'         # Promoter
DNA += 'BB'             # Bind DNA
DNA += 'AA BBBABBBA AA' # With QPQP
DNA += 'BA'             # Ribosome
DNA += 'ACAA'           # ATPase
DNA += 'DDAAAA'         # End

DNA += 'ADDADD'         # Promoter
DNA += 'BB'             # Bind DNA
DNA += 'AA BBBBBBBA AA' # With QQQP
DNA += 'DDAAAA'         # End

solution = virtualCell.Solution(10000.0)
cell = solution.addCell(1000.0)
cell.metabolites['EH'].amount += 80     # Add ATP
cell.metabolites['JG'].amount += 80     # Add Amino acids

cell.addDNA(DNA)
cell.addProtein('QLQPQPLPNL', 2.0)

#print "\n -Proteins-"
#cell.output('proteins')
#cell.output('metabolites')

sim_time = 5001
data_collection_functions = {\
    #'ribosome':  (lambda cell: cell.proteins['QLQPQPLPNL'].amount),
    #'repressor': (lambda cell: cell.proteins['QLQQQPL'].amount)}#,
    'tf on tf': (lambda cell: cell.proteins['QLQPQPLPNL'].binding_domains[0].targets[cell.genes[0]][1]),
    'tf on in': (lambda cell: cell.proteins['QLQPQPLPNL'].binding_domains[0].targets[cell.genes[1]][1]),
    'in on tf': (lambda cell: cell.proteins['QLQQQPL'].binding_domains[0].targets[cell.genes[0]][1]),
    'in on in': (lambda cell: cell.proteins['QLQQQPL'].binding_domains[0].targets[cell.genes[1]][1])}
    #'ribosome occupancy': (lambda cell: cell.genes[0].occupancy, []))}

data_collection = dict([(key, []) for key in data_collection_functions.keys()])

for t in range(sim_time):
    cell.metabolites['EH'].amount = 80
    solution.update()
    for d in data_collection.keys():
        data_collection[d].append(data_collection_functions[d](cell))

for k, v in data_collection.items():
    print k, v[-1]
   
print "\n -Proteins-"    
cell.output('proteins')
cell.output('metabolites')

g = drawSVGGraph.Graph()
g.x_axis_label = "Time"
g.data = data_collection
print g.data.keys()

g.outputSVG('test', width=400, height=300)