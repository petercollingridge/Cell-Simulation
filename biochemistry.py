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
        self.interpretSequence2()

    def interpretSequence2(self):
        self.functions.append(self.catalyse)
        enz_func = None

        n = 1
        while n < len(self.sequence):
            codon = self.sequence[n-1] + self.sequence[n]

            if enz_func == None:
                if codon == 'BA':
                    enz_func = 'tf'
                elif codon == 'BB':
                    enz_func = 'tr'
                if codon == 'BC':
                    enz_func = 'ef'
                elif codon == 'BD':
                    enz_func = 'er'

    # Transporters
            elif enz_func[0] == 't':
                m = codon_to_metabolite[codon]
                print 'transporter', m

                if enz_func[1] == 'f':
                    self.setMetabolites([m], [m], self.solution.solution)
                else:
                    self.setMetabolites([m], [m], self.solution, self.solution.solution)
                enz_func = None

    # Enzymes
            elif enz_func[0] == 'e':
                r = all_reactions[codon]
                print 'enzyme', r.substrates

                if enz_func[1] == 'f':
                    self.setMetabolites(r.substrates, r.products)
                    self.f_rate *= r.rates[0]
                    self.r_rate *= r.rates[1]
                else:
                    self.setMetabolites([m], [m], self.solution, self.solution.solution)
                enz_func = None

            n += 2

    def interpretSequence(self):
        seq = self.sequence.split('-')
        catalytic = False

        n = 0
        while n < len(seq):
            if seq[n] == 'tra':
                n += 2
                catalytic = True

                if seq[n-1] == 'f':
                    self.setMetabolites([seq[n]], [seq[n]], self.solution.solution)
                else:
                    self.setMetabolites([seq[n]], [seq[n]], self.solution, self.solution.solution)

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
all_metabolites = 'E,F,G,H,I,J,K,L,EH,EL,FG,FK,IL,IH,JK,JG'.split(',')
codons = 'AA,AB,AC,AD,BA,BB,BC,BD,CA,CB,CC,CD,DA,DB,DC,DD'.split(',')

codon_to_metabolite = dict(zip(codons, all_metabolites))

all_reactions = {'AA': Reaction(['EH'], ['E', 'H'], 1, 0.2), 
                 'AB': Reaction(['EL'], ['E', 'L'], 1, 0.5),                  'AC': Reaction(['FG'], ['F', 'G'], 0.85, 1), 
                 'AD': Reaction(['FK'], ['F', 'K'], 0.3, 1), 
                 'BA': Reaction(['IL'], ['I', 'L'], 0.8, 1), 
                 'BB': Reaction(['IH'], ['I', 'H'], 1, 0.5), 
                 'BC': Reaction(['JK'], ['J', 'K'], 0.07, 1), 
                 'BD': Reaction(['JG'], ['J', 'G'], 0.3, 1), 
                 'CA': Reaction(['EH','IL'], ['EL', 'IH'], 1, 1), 
                 'CB': Reaction(['FG','JK'], ['FK', 'JG'], 1, 1)}
