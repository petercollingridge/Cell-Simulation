import virtualCell

def determineBinding(cell):
    total_protein = sum([protein.amount for protein in cell.proteins.values()])

    for protein in cell.proteins.values():
        p = protein.amount/(total_protein+total_RNA + 20.0)
        
        for domain in protein.binding_domains:
            print domain.sequence
            for target, sites in domain.targets.items():
                print target.sequence,
                print "Each site binds", target.amount*p/len(sites)

DNA  = 'AADADD'         # Promoter
DNA += 'BB'             # Bind DNA
DNA += 'AA BBBABBBA AA' # At QPQP
DNA += 'ACCC'           # DNAse
DNA += 'ADAA'           # ATPase
DNA += 'DDAA'           # End

DNA += 'ADADAD'         # Promoter
DNA += 'AA CB DD'       # EL pore

solution = virtualCell.Solution(10000.0)
cell = solution.addCell(1000.0)
cell.addDNA(DNA)
cell.addProtein('QLQPQPLNVOL', 1.0)

print "\n-Proteins-"
cell.output('proteins')
print

# Find binding sites:
for protein in cell.proteins.values():
    for domain in protein.binding_domains:
        domain.findPromoterStrengths(cell.genes)