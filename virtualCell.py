import biochemistry

class Solution():
    def __init__(self, volume):
        self.volume = volume
        self.cells = []
        self.proteins = {}
        self.metabolites = {}

        for m in biochemistry.all_metabolites:
            self.metabolites[m] = biochemistry.Metabolite(m, self.volume)

    def addDefaultMetabolites(self):
        n = 0.08
        for m in biochemistry.all_metabolites[:8]:
            self.metabolites[m].amount = n * self.volume
            n /= 2.0

    def addCell(self, volume):
        newCell = Cell(volume, self)
        self.cells.append(newCell)

    def output(self):
        metabolites = self.metabolites.keys()
        metabolites.sort()

        for m in metabolites:
            print '%s\t%.3f%%' % (m, 100*self.metabolites[m].amount/self.volume)

class Cell(Solution):
    def __init__(self, volume, solution):
        Solution.__init__(self, volume)
        self.solution = solution

    def interpretDNA(self):
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
