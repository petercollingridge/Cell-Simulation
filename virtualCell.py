import biochemistry

default_metabolites = dict([(m, 0.08/2 ** i) for i, m in enumerate(biochemistry.all_metabolites[:8])])

class Solution():
    def __init__(self, volume):
        self.volume = volume
        self.cells = []
        self.proteins = {}
        self.metabolites = dict([(m, biochemistry.Metabolite(m, self.volume)) for m in biochemistry.all_metabolites])

    def setMetabolites(self, metabolites='default'):
        if metabolites == 'default':
            metabolites = default_metabolites

        for m in metabolites:
            self.metabolites[m].amount = metabolites[m] * self.volume

    def addCell(self, volume):
        newCell = Cell(volume, self)
        self.cells.append(newCell)
        
    def update(self, ticks=1):
        for t in range(ticks):
            for cell in self.cells:
                cell.update()

    def output(self, output_type):
        if output_type == 'proteins':
            for protein in self.proteins.values():
                protein.outputProperties()

                if protein.substrates:
                    print "Reaction:"
                    
                    for s in protein.substrates:
                        print "  %s" % s.name,

                    print '->',

                    for p in protein.products:
                        print p.name,
                        
                print '\n'

        elif output_type == 'metabolites':
            metabolites = self.metabolites.keys()
            metabolites.sort()

            for m in metabolites:
                print '%s\t%.4f%%' % (m, 100*self.metabolites[m].amount/self.volume)

class Cell(Solution):
    def __init__(self, volume, solution):
        Solution.__init__(self, volume)
        self.solution = solution    # Solution in which the cell exists
        self.DNA = []
        self.RNA = {}
        self.genes = []
        self.new_protein = 0.0

    def addDNA(self, DNA_string):
        DNA = DNA_string.rstrip('\n').replace(' ', '')
        self.DNA.append(DNA)
        
        genes = DNA.split('DDAA')
        self.genes.extend(genes)
        
        for gene in genes:
            if len(gene) > 0:
                peptide = biochemistry.Translate(gene)
                print gene, peptide
                self.addProtein(peptide, 0.0)
                
    def addRNA(self, RNA, amount):
        self.RNA[RNA] = self.RNA.get(RNA, 0.0) + amount

    def addProtein(self, protein, amount):
        if protein not in self.proteins:
            self.proteins[protein] = biochemistry.Protein(protein, self)
        self.proteins[protein].amount += amount

    def update(self):
        # Test protein binding RNA, DNA, protein
        
        for p in self.proteins.values():
            p.update()
        self.new_protein /= len(self.proteins.values())

        for p in self.proteins.values():
            p.amount += self.new_protein / p.length
        self.new_protein = 0