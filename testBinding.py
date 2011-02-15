import virtualCell

DNA  = 'BB AC'          # bind RNA
DNA += 'AA BBBABBBA AA' # At QPQP
DNA += 'ACCD'           # RNAse
DNA += 'ADAA'           # ATPase
DNA += 'DDAA'           # End

DNA += 'BB AB'          # bind DNA
DNA += 'AA BBBABBBA AA' # At QPQP
DNA += 'ACCC'           # DNAse
DNA += 'ADAA'           # ATPase
DNA += 'DD'             # End

solution = virtualCell.Solution(10000.0)
cell = solution.addCell(1000.0)
cell.addDNA(DNA)

print "\n-Proteins-"
cell.output('proteins')