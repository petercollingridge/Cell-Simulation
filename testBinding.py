import virtualCell
from bindingInteractions import findBindingSites

def determineBinding(cell):
    total_protein = sum([protein.amount for protein in cell.proteins.values()])
    total_RNA = sum([RNA.amount for RNA in cell.RNA.values()])

    for protein in cell.proteins.values():
        p = protein.amount/(total_protein+total_RNA + 20.0)
        
        for domain in protein.binding_domains:
            print domain.sequence
            for target, sites in domain.targets.items():
                print target.sequence,
                print "Each site binds", target.amount*p/len(sites)

DNA  = 'BB AC'          # Bind RNA
DNA += 'AA CCCBABAB AA' # At QPQP VUMM
DNA += 'ACCD'           # RNAse
DNA += 'ADAA'           # ATPase
DNA += 'DDAA'           # End

DNA += 'BB AB'          # Bind DNA
DNA += 'AA BBBABBBA AA' # At QPQP
DNA += 'ACCC'           # DNAse
DNA += 'ADAA'           # ATPase
DNA += 'DD'             # End

solution = virtualCell.Solution(10000.0)
cell = solution.addCell(1000.0)
cell.addDNA(DNA)
cell.addRNA('BABAAABBACAABBBABBBAAAACCDADDDAA', 1.5)
cell.addProtein('QMLQPQPLNVOL', 1.0)
cell.addProtein('QNLVUMMLNWOL', 2.0)

print "\n-Proteins-"
cell.output('proteins')
print

# Find binding sites:
for protein in cell.proteins.values():
    for domain in protein.binding_domains:
        if domain.type == 'RNA':
            for sequence, RNA in cell.RNA.items():
                sites = findBindingSites(domain.sequence, sequence)
                if sites:
                    domain.targets[RNA] = sites
        elif domain.type == 'DNA':
            for DNA in cell.DNA:
                sites = findBindingSites(domain.sequence, DNA)
                if sites:
                    domain.targets[DNA] = sites
