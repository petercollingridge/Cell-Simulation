import biochemistry

default_metabolites = dict([(m, 0.08/2 ** i) for i, m in enumerate(biochemistry.all_metabolites[:8])])

class Solution():
    def __init__(self, volume, metabolites='default'):
        self.volume = volume
        self.DNA = []
        self.cells = []
        self.proteins = {}
        
        self.metabolites = dict([(m, biochemistry.Metabolite(m, self.volume)) for m in biochemistry.all_metabolites])
        metabolite_dict = metabolites=='default' and default_metabolites or metabolites
        self._setMetabolites(metabolite_dict)

    def _setMetabolites(self, metabolites):
        for name, amount in metabolites.items():
            self.metabolites[name].amount = amount * self.volume

    def addCell(self, volume, metabolites='default'):
        new_cell = Cell(volume, self, metabolites)
        self.cells.append(new_cell)
        return new_cell
        
    def update(self, ticks=1):
        for t in range(ticks):
            for cell in self.cells:
                cell.update()

    def output(self, output_type):
        if output_type == 'proteins':
            for protein in self.proteins.values():
                protein.output()
                
        elif output_type == 'metabolites':
            metabolites = self.metabolites.keys()
            metabolites.sort()

            for m in metabolites:
                print '%s\t%.4f%%' % (m, self.metabolites[m].concentration())
                
        elif output_type == 'cells':
            print "%d cells" % len(self.cells)
            
            for cell in self.cells:
                cell.output('proteins')

class Cell(Solution):
    def __init__(self, volume, solution, metabolites):
        Solution.__init__(self, volume, metabolites)
        self.solution = solution    # Solution in which the cell exists
        self.genes = []
        self.new_protein = 0.0
        
        for name, metabolite in self.metabolites.items():
            metabolite.name = "%s(in)" % name
        self.metabolites['protein'] = biochemistry.Metabolite('protein', self.volume)

    def addDNA(self, DNA_string):
        DNA = DNA_string.rstrip().replace(' ', '')
        self.DNA.append(DNA)
        
        for gene_seq in DNA.split('DDAA'):
            if len(gene_seq) > 6:
                gene = biochemistry.Gene(gene_seq)
                self.genes.append(gene)
                peptide = biochemistry.Translate(gene.ORF)
                print "DNA: %s -> %s" % (gene.ORF, peptide)
                self.addProtein(peptide, 0.0)

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