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

    def output(self, output_type):
        if output_type == 'proteins':
            for p in self.proteins:
                print self.proteins[p].amount, p

                for s in self.proteins[p].substrates:
                    print s.name,

                print '->',

                for p in self.proteins[p].products:
                    print p.name,
                print

        elif output_type == 'metabolites':
            metabolites = self.metabolites.keys()
            metabolites.sort()

            for m in metabolites:
                print '%s\t%.4f%%' % (m, 100*self.metabolites[m].amount/self.volume)

class Cell(Solution):
    def __init__(self, volume, solution):
        Solution.__init__(self, volume)
        self.solution = solution
        self.new_protein = 0.0

    def interpretDNA(self):
        self.DNA = self.DNA.replace(' ', '')
        proteins = self.DNA.split('DDAA')
        
        for p in proteins:
            if len(p) > 0:
                self.addProtein(p, 0.0)

    def addProtein(self, protein, amount):
        if protein not in self.proteins:
            self.proteins[protein] = biochemistry.Protein(protein, self)
        self.proteins[protein].amount += amount

    def update(self):

        for p in self.proteins.values():
            p.update()
        self.new_protein /= len(self.proteins.values())

        for p in self.proteins.values():
            p.amount += self.new_protein / p.length
        self.new_protein = 0

defaultMetabolites = {}
metabolite_conc = 0.08
for m in biochemistry.all_metabolites[:8]:
    defaultMetabolites[m] = metabolite_conc
    metabolite_conc /= 2.0
