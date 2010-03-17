# Define all the metabolites that will exist
all_metabolites = ['AB', 'A', 'B']

class Metabolite:
    def __init__(self, name):
        self.name = name
        self.amount = 0.0

class Reaction:
    def __init__(self, substrates, products, forward_rate, reverse_rate):
        self.substrates = substrates
        self.products = products
        self.rates = (forward_rate, reverse_rate)

class Solution():
    def __init__(self, volume):
        self.volume = volume
        self.cells = []
        self.proteins = {}
        self.metabolites = {}

        for m in all_metabolites:
            self.metabolites[m] = Metabolite(m)

    def addCell(self, volume):
        newCell = Cell(volume)
        newCell.solution = self
        self.cells.append(newCell)

class Cell(Solution):
    def addProtein(self, protein, amount):

        if protein not in self.proteins:
            self.proteins[protein] = Protein(protein, self)
        self.proteins[protein].amount += amount

    def update(self):
        print 'Cell has %d proteins' % len(self.proteins.keys())

        for p in self.proteins.values():
            p.update()

class Protein():
    def __init__(self, sequence, solution):
        self.sequence = sequence
        self.solution = solution
        self.amount = 0.0
        self.rate = 1.0
        self.functions = []
        self.interpretSequence()

    def interpretSequence(self):
        temp = self.sequence.split('-')

        if temp[0] == 'transporter':
            self.functions.append(self.transport)
        if len(temp) > 1:
            self.setMetabolites([temp[1]])

    def setMetabolites(self, substrates, products=[]):
        self.substrates = []
        self.products = []

        for s in substrates:
            self.substrates.append(self.solution.metabolites[s])
            self.products.append(self.solution.solution.metabolites[s])

        for p in products:
            self.products.append(self.solution.metabolites[p])
            self.substrates.append(self.solution.solution.metabolites[p])

    def transport(self):
        conc1 = self.substrates[0].amount / self.solution.volume
        conc2 = self.products[0].amount / self.solution.solution.volume
        rate = (conc1 - conc2) * self.rate * self.amount

        for s in self.substrates:
            s.amount -= rate
        for p in self.products:
            p.amount += rate

    def update(self):
        for function in self.functions:
            function()

ATPase = Reaction(['AB'], ['A', 'B'], 0.1, 0.0001)
all_reactions = [ATPase]
