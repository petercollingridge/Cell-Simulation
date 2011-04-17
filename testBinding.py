import virtualCell

DNA  = 'AADADD'         # Promoter
DNA += 'BB'             # Bind DNA
DNA += 'AA BBBABBBA AA' # At QPQP
DNA += 'BA'             # Ribosome
DNA += 'ACAA'           # ATPase
DNA += 'DDAAAA'         # End

DNA += 'AADAAD'         # Promoter
DNA += 'AA CB DD'       # EL pore

solution = virtualCell.Solution(10000.0)
cell = solution.addCell(1000.0)
cell.metabolites['EH'].amount += 80     # Add ATP
cell.metabolites['JG'].amount += 80     # Add Amino acids

cell.addDNA(DNA)
cell.addProtein('QLQPQPLPNL', 1.0)

print "\n -Proteins-"
#cell.output('proteins')
#cell.output('metabolites')

solution.update(20)
cell.output('proteins')
cell.output('metabolites')
