# Define all the metabolites that will exist
all_metabolites = ['ATP', 'ADP', 'Phosphates']

class Reaction:
    def __init__(self, substrates, products, forward_rate, reverse_rate):

        self.substrates = substrates
        self.products = products
        self.rates = (forward_rate, reverse_rate)

class Solution():
    def __init__(self, volume):
        self.volume = volume
        self.proteins = {}
        self.metabolites = {}

        for m in all_metabolites:
            self.metabolites[m] = 0.0

class Cell(Solution):
    def addProtein(self, protein, amount):

        if protein not in self.proteins:
            self.proteins[protein] = Protein(protein)

        self.proteins[protein].amount += amount

    def update(self):
        print 'Cell has %d proteins' % len(self.proteins.keys())

        for p in self.proteins.values():
            p.update()

class Protein():
    def __init__(self, sequence):
        self.sequence = sequence
        self.amount = 0.0
        self.interpretSequence()

    def interpretSequence(self):
        temp = self.sequence.split('-')

        if len(temp) > 1:
            self.setMetabolites(temp[1])
        if temp[0] == 'transporter':
            

    def setMetabolites(self, substrates, products=None):
        self.substrates = substrates
        self.products = products

    def update(self):
        print 'Protein has no function'


ATPase = Reaction(['ATP'], ['ADP', 'Phosphates'], 0.1, 0.0001)
all_reactions = [ATPase]
