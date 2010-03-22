class Metabolite:
    def __init__(self, name, volume):
        self.name = name
        self.amount = 0.0
        self.volume = volume

class Reaction:
    def __init__(self, substrates, products, forward_rate, reverse_rate):
        self.substrates = substrates
        self.products = products
        self.rates = (forward_rate, reverse_rate)

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
            self.functions.append(self.catalyse)
            if len(temp) > 1:
                self.setMetabolites(self.solution.solution, [temp[1]], self.solution, [temp[1]])

        elif temp[0] == 'enzyme':
            self.functions.append(self.catalyse)
            if len(temp) > 1:
                self.setMetabolites(self.solution, all_reactions[temp[1]].substrates, self.solution, all_reactions[temp[1]].products)

    def setMetabolites(self, solution1, substrates, solution2, products):
        self.substrates = []
        self.products = []

        for s in substrates:
            self.substrates.append(solution1.metabolites[s])

        for p in products:
            self.products.append(solution2.metabolites[p])

    def catalyse(self):
        substrate_bound = 1.0
        product_bound = 1.0

        for s in self.substrates:
            substrate_bound *= s.amount / s.volume
            #print s.name,

        #print '->',

        for p in self.products:
            product_bound *= p.amount / p.volume
         #   print p.name,

        net_rxn = (substrate_bound - product_bound) * self.rate * self.amount
        #print net_rxn

        for s in self.substrates:
            s.amount -= net_rxn
        for p in self.products:
            p.amount += net_rxn

    def update(self):
        for function in self.functions:
            function()

# Define all the metabolites that exist
all_metabolites = ['AB', 'A', 'B']
all_reactions = {'ABase': Reaction(['AB'], ['A', 'B'], 0.1, 0.0001)}
