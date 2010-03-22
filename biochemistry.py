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
        self.f_rate = 1.0
        self.r_rate = 1.0
        self.functions = []
        self.substrates = []
        self.products = []
        self.interpretSequence()

    def interpretSequence(self):
        seq = self.sequence.split('-')
        catalytic = False

        n = 0
        while n < len(seq):
            if seq[n] == 'tra':
                n += 1
                catalytic = True
                self.setMetabolites([seq[n]], [seq[n]], self.solution.solution)

            elif seq[n] == 'rxn':
                n += 2
                catalytic = True

                if seq[n-1] == 'f':
                    self.setMetabolites(all_reactions[seq[n]].substrates, all_reactions[seq[n]].products)
                    self.f_rate *= all_reactions[seq[n]].rates[0]
                    self.r_rate *= all_reactions[seq[n]].rates[1]
                else:
                    self.setMetabolites(all_reactions[seq[n]].products, all_reactions[seq[n]].substrates)
                    self.f_rate *= all_reactions[seq[n]].rates[1]
                    self.r_rate *= all_reactions[seq[n]].rates[0]
            n += 1

        if catalytic: self.functions.append(self.catalyse)

    def setMetabolites(self, substrates, products, sol1=None, sol2=None):
        if sol1 == None: sol1 = self.solution
        if sol2 == None: sol2 = self.solution

        for s in substrates:
            self.substrates.append(sol1.metabolites[s])

        for p in products:
            self.products.append(sol2.metabolites[p])

    def catalyse(self):
        substrate_bound = 1.0
        product_bound = 1.0

        for s in self.substrates:
            substrate_bound *= s.amount / s.volume
        #    print s.name,

        #print '->',

        for p in self.products:
            product_bound *= p.amount / p.volume
        #    print p.name,

        net_rxn = (substrate_bound*self.f_rate - product_bound*self.r_rate) * self.amount
        #print "\t%.4f" % net_rxn

        for s in self.substrates:
            s.amount -= net_rxn
        for p in self.products:
            p.amount += net_rxn

    def update(self):
        for function in self.functions:
            function()

# Define all the metabolites that exist
all_metabolites = ['A', 'B', 'C','D', 'AB', 'CD']
all_reactions = {'ABase': Reaction(['AB'], ['A', 'B'], 0.5, 1), 
                 'CDase': Reaction(['CD'], ['C', 'D'], 1, 0.25)}
