import biochemistry

class Solution():
    def __init__(self, volume):
        self.volume = volume
        self.cells = []
        self.proteins = {}
        self.metabolites = {}

        for m in biochemistry.all_metabolites:
            self.metabolites[m] = biochemistry.Metabolite(m, self.volume)

    def addCell(self, volume):
        newCell = Cell(volume)
        newCell.solution = self
        self.cells.append(newCell)

    def output(self):
        print
        for m in self.metabolites.keys():
            print '%s\t%.2f mM' % (m, 1000*self.metabolites[m].amount/self.volume)

class Cell(Solution):
    def addProtein(self, protein, amount):

        if protein not in self.proteins:
            self.proteins[protein] = biochemistry.Protein(protein, self)
        self.proteins[protein].amount += amount

    def update(self):
        for p in self.proteins.values():
            p.update()

