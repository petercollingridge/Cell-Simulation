import biochemistry

class Solution():
    def __init__(self, volume):
        self.volume = volume
        self.cells = []
        self.proteins = {}
        self.metabolites = {}

        for m in biochemistry.all_metabolites:
            self.metabolites[m] = biochemistry.Metabolite(m, self.volume)

    def setMetabolites(self, metabolites):
        if metabolites == 'default':
            metabolites = defaultMetabolites

        for m in metabolites:
            self.metabolites[m].amount = metabolites[m] * self.volume

    def addCell(self, volume):
        newCell = Cell(volume, self)
        self.cells.append(newCell)

    def outputProteins(self):
        for p in self.proteins:
            print '\n', self.proteins[p].amount, p

            for s in self.proteins[p].substrates:
                print s.name,

            print '->',

            for p in self.proteins[p].products:
                print p.name,
            print

    def output(self):
        metabolites = self.metabolites.keys()
        metabolites.sort()

        for m in metabolites:
            print '%s\t%.4f%%' % (m, 100*self.metabolites[m].amount/self.volume)

class Cell(Solution):
    def __init__(self, volume, solution):
        Solution.__init__(self, volume)
        self.solution = solution

    def interpretDNA(self):
        self.DNA = self.DNA.replace(' ', '')
        proteins = self.DNA.split('DDAA')
        protein_amount = 16.0 / len(proteins)
        
        for p in proteins:
            self.addProtein(p, protein_amount)

    def addProtein(self, protein, amount):
        if protein not in self.proteins:
            self.proteins[protein] = biochemistry.Protein(protein, self)
        self.proteins[protein].amount += amount

    def update(self):
        for p in self.proteins.values():
            p.update()

defaultMetabolites = {}
metabolite_conc = 0.08
for m in biochemistry.all_metabolites[:8]:
    defaultMetabolites[m] = metabolite_conc
    metabolite_conc /= 2.0
