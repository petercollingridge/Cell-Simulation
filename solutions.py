import biochemistry

default_metabolites = dict([(m, 0.08/2 ** i) for i, m in enumerate(biochemistry.CHEMICALS[:8])])

class Solution():
    def __init__(self, volume, metabolites='default'):
        self.volume = volume
        self.DNA = []
        self.cells = []
        self.proteins = {}
        
        self.metabolites = dict([(m, biochemistry.Metabolite(m, self.volume)) for m in biochemistry.CHEMICALS])
        metabolite_dict = metabolites=='default' and default_metabolites or metabolites
        self._setMetabolites(metabolite_dict)
        
        for name, metabolite in self.metabolites.items():
            metabolite.name = "%s(out)" % name

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

    def output(self, output_type='all'):
        if output_type == 'proteins' or output_type == 'all':
            print "\n-Proteins-"
            for protein in self.proteins.values():
                protein.output()
                
        elif output_type == 'metabolites' or output_type == 'all':
            print "\n-Metabolites-"
            metabolites = self.metabolites.keys()
            metabolites.sort()

            for m in metabolites:
                print '%s\t%.4f%%' % (m, self.metabolites[m].concentration())
                
        elif output_type == 'cells':
            print "%d cells" % len(self.cells)
            
            for cell in self.cells:
                cell.output('proteins')

class Cell(Solution):
    def __init__(self, volume, solution, metabolites='default'):
        Solution.__init__(self, volume, metabolites)
        self.solution = solution    # Solution in which the cell exists
        self.genes = []
        
        for name, metabolite in self.metabolites.items():
            metabolite.name = "%s(in)" % name

    def addDNA(self, DNA_string):
        DNA = DNA_string.rstrip().replace(' ', '')
        self.DNA.append(DNA)
        
        for gene_seq in DNA.split('DDAAAA'):
            if len(gene_seq) > 6:
                gene = biochemistry.Gene(gene_seq)
                if len(gene.protein_code) > 1:
                    self.genes.append(gene)
                
        for gene in self.genes:
            self.addProtein(gene.protein_code, 0.0)
            #print "DNA: %s -> %s" % (gene.ORF, peptide)

    def addProtein(self, protein, amount):
        if protein not in self.proteins:
            self.proteins[protein] = biochemistry.Protein(protein, self)
        self.proteins[protein].amount += amount

    def update(self):
        for p in self.proteins.values():
            p.update()
