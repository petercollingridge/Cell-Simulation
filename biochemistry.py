from bindingInteractions import findBindingSites

def Translate(mRNA):
    """ Takes a DNA sequence (using nucleotides: A,B,C,D)
        Returns a peptide sequence (using amino acids L-Z) """
        
    peptide = ''
    
    # Splits bases into pairs and cuts off final base if there is an odd number
    for n in range(1, len(mRNA), 2):        
        if mRNA[n-1:n+1] == 'DD': return peptide
        peptide += TRANSLATE[mRNA[n-1:n+1]]
        
    return peptide

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
        self.length   = len(sequence)
        self.solution = solution
        
        self.degradation_rate = 0.00001
        self.amount = 0.0
        
        self.f_rate = 1.0
        self.r_rate = 1.0
        self.net_rxn = 0

        self.functions = [self.degrade]
        self.substrates = []
        self.products = []
        self.binding_sites = []
        
        self.interpretSequence()

    def interpretSequence(self):
        ribosome  = False
        catalytic = False
        enz_func = None

        n = 1
        while n < len(self.sequence):
            codon = self.sequence[n-1] + self.sequence[n]

    # Find enzyme function
            if enz_func == None:
                if codon in codon_to_function:
                    enz_func = codon_to_function[codon]

                    if enz_func == 'ribosome':
                        ribosome = True
                        enz_func = None
                        self.r_rate *= 0.25
                        self.substrates.append(self.solution.metabolites['JG'])
                        
                    elif enz_func == 'bind_DNA':
                        binding_seq = ''

    # Transporters
            elif enz_func[0] == 't':
                catalytic = True
                m = codon_to_metabolite[codon]

                if enz_func[1] == 'f':
                    self.setMetabolites([m], [m], self.solution.solution)
                else:
                    self.setMetabolites([m], [m], self.solution, self.solution.solution)
                enz_func = None

    # Enzymes
            elif enz_func[0] == 'e':
                if codon in all_reactions.keys():
                    catalytic = True
                    r = all_reactions[codon]

                    if enz_func[1] == 'f':
                        self.setMetabolites(r.substrates, r.products)
                        self.f_rate *= r.rates[0]
                        self.r_rate *= r.rates[1]
                    else:
                        self.setMetabolites(r.products, r.substrates)
                        self.f_rate *= r.rates[1]
                        self.r_rate *= r.rates[0]
                    enz_func = None
                    
            elif enz_func == 'bind_DNA':
                if codon != 'DD':
                    binding_seq += codon
                else:
                    binding_sites.append(binding_seq)
                    enz_func = None

            if ribosome:
                self.functions.extend([self.find_reaction_rate, self.translate])
            elif catalytic:
                self.functions.extend([self.find_reaction_rate, self.catalyse])
            n += 2

    def setMetabolites(self, substrates, products, sol1=None, sol2=None):
        if sol1 == None: sol1 = self.solution
        if sol2 == None: sol2 = self.solution

        for s in substrates:
            self.substrates.append(sol1.metabolites[s])

        for p in products:
            self.products.append(sol2.metabolites[p])

    def outputReaction(self):
        for s in self.substrates:
            print s.name,
        print '->',

        for p in self.products:
            print p.name,
        print "\t%f" % self.net_rxn

    def degrade(self):
        degradation = self.amount * self.degradation_rate
        self.amount -= degradation
        self.solution.metabolites['JG'].amount += degradation

    def find_reaction_rate(self):
        substrate_bound = self.f_rate
        product_bound = self.r_rate

        for s in self.substrates:
            substrate_bound *= s.amount / s.volume
        for p in self.products:
            product_bound *= p.amount / p.volume
 
        self.net_rxn = (substrate_bound - product_bound) * self.amount

    def catalyse(self):
        for s in self.substrates:
            s.amount -= self.net_rxn
        for p in self.products:
            p.amount += self.net_rxn

    def translate(self):
        if self.net_rxn > 0:
            for s in self.substrates:
                s.amount -= self.net_rxn
            for p in self.products:
                p.amount += self.net_rxn

            self.solution.new_protein += self.net_rxn

    def update(self):
        for function in self.functions:
            function()

# Map codons to enzyme functions
nucleotides = ['A', 'B', 'C', 'D']
amino_acids = 'L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z, '.split(',')
all_metabolites = 'E,F,G,H,I,J,K,L,EH,EL,FG,FK,IL,IH,JK,JG'.split(',')
enzyme_functions = 'tf,tr,ef,er,ribosome,bind_DNA'.split(',')
codons = ['%s%s' % (a, b) for a in nucleotides for b in nucleotides]

TRANSLATE = dict(zip(codons, amino_acids))
codon_to_metabolite = dict(zip(codons, all_metabolites))
codon_to_function = dict(zip(codons[4:], enzyme_functions))

all_reactions = {'AA': Reaction(['EH'], ['E', 'H'], 1, 0.2), 
                 'AB': Reaction(['EL'], ['E', 'L'], 1, 0.5), 
                 'AC': Reaction(['FG'], ['F', 'G'], 0.85, 1), 
                 'AD': Reaction(['FK'], ['F', 'K'], 0.3, 1), 
                 'BA': Reaction(['IL'], ['I', 'L'], 0.8, 1), 
                 'BB': Reaction(['IH'], ['I', 'H'], 1, 0.5), 
                 'BC': Reaction(['JK'], ['J', 'K'], 0.07, 1), 
                 'BD': Reaction(['JG'], ['J', 'G'], 0.3, 1), 
                 'CA': Reaction(['EH','IL'], ['EL', 'IH'], 1, 1), 
                 'CB': Reaction(['FG','JK'], ['FK', 'JG'], 1, 1),
                 'CC': Reaction(['protein'], ['JG'], 1, 0.25)}