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
    def __init__(self, name, volume=100.0):
        self.name = name
        self.volume = volume
        self.amount = 0.0
        
    def concentration(self):
        return 100.0 * self.amount / self.volume

class Reaction:
    def __init__(self, substrates, products, forward_rate, reverse_rate):
        self.substrates = substrates
        self.products = products
        self.rates = (forward_rate, reverse_rate)

class RNA:
    def __init__(self, sequence, amount=0.0):
        self.sequence = sequence
        self.amount = amount
        self.sites = {}
        
class BindingDomain:
    def __init__(self, sequence, type):
        self.sequence = sequence
        self.type = type
        self.targets = {}
    
class Protein:
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
        self.binding_domains = []
        self.substrates = []
        self.products = []
        
        self._interpretSequence()

    def _interpretSequence(self):
        ribosome  = False
        catalytic = False
        domain = None
        binding_seq = ''
        binding_partner = None

        for aa in self.sequence:

        # Find enzyme function
            if domain == None:
                domain = aa_to_function.get(aa)
                #print 'Found domain ', domain

                if domain == 'ribosome':
                    ribosome = True
                    domain = None
                    self.r_rate *= 0.25
                    self.substrates.append(self.solution.metabolites['JG'])

        # Transporters
            elif domain[0] == 't':
                catalytic = True
                m = aa_to_metabolite[aa]

                if domain[1] == 'f':
                    self.setMetabolites([m], [m], self.solution.solution)
                else:
                    self.setMetabolites([m], [m], self.solution, self.solution.solution)
                domain = None

        # Enzymes
            elif domain[0] == 'e':
                if aa in aa_to_reaction.keys():
                    catalytic = True
                    r = aa_to_reaction[aa]

                    if domain[1] == 'f':
                        self.setMetabolites(r.substrates, r.products)
                        self.f_rate *= r.rates[0]
                        self.r_rate *= r.rates[1]
                    else:
                        self.setMetabolites(r.products, r.substrates)
                        self.f_rate *= r.rates[1]
                        self.r_rate *= r.rates[0]
                    domain = None

        # Binding Proteins
            elif domain == 'binding':
                if aa == 'L':
                    domain = 'binding sequence'
                    binding_seq = ''
                    
                elif aa == 'M':
                    binding_partner = 'DNA'
                elif aa == 'N':
                    binding_partner = 'RNA'
                    
            elif domain == 'binding sequence':
                if aa == 'L':
                    if binding_seq and binding_partner:
                        self.binding_domains.append(BindingDomain(binding_seq, binding_partner))
                        domain = None
                else:
                    binding_seq += aa

            if ribosome:
                self.functions.extend([self.find_reaction_rate, self.translate])
            elif catalytic:
                self.functions.extend([self.find_reaction_rate, self.catalyse])

    def setMetabolites(self, substrates, products, sol1=None, sol2=None):
        if sol1 == None: sol1 = self.solution
        if sol2 == None: sol2 = self.solution

        for s in substrates:
            self.substrates.append(sol1.metabolites[s])

        for p in products:
            self.products.append(sol2.metabolites[p])

    def output(self):
        print "Sequence: %s" % self.sequence
        print "Amount:   %s" % self.amount
        
        if self.substrates: self._outputReaction()
        if self.binding_domains: self._outputBindingProperties()
        print

    def _outputReaction(self):
        print "Catalyses:"
        print " %s -> %s" % (' + '.join([s.name for s in self.substrates]), ' + '.join([p.name for p in self.products]))
        #print "\t%f" % self.net_rxn
            
    def _outputBindingProperties(self):
        for site in self.binding_domains:
            print "Binds %s with sequence %s" % (site.type, site.sequence)

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
codons = ['%s%s' % (a, b) for a in nucleotides for b in nucleotides]

amino_acids = 'L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z, '.split(',')
all_metabolites = 'E,F,G,H,I,J,K,L,EH,EL,FG,FK,IL,IH,JK,JG'.split(',')
enzyme_functions = 'tf,tr,ef,er,ribosome,binding'.split(',')
all_reactions = [Reaction(['EH'], ['E', 'H'], 1, 0.2), 
                 Reaction(['EL'], ['E', 'L'], 1, 0.5), 
                 Reaction(['FG'], ['F', 'G'], 0.85, 1), 
                 Reaction(['FK'], ['F', 'K'], 0.3, 1), 
                 Reaction(['IL'], ['I', 'L'], 0.8, 1), 
                 Reaction(['IH'], ['I', 'H'], 1, 0.5), 
                 Reaction(['JK'], ['J', 'K'], 0.07, 1), 
                 Reaction(['JG'], ['J', 'G'], 0.3, 1), 
                 Reaction(['EH','IL'], ['EL', 'IH'], 1, 1), 
                 Reaction(['FG','JK'], ['FK', 'JG'], 1, 1),
                 Reaction(['protein'], ['JG'], 1, 0.25),
                 Reaction(['RNA'], ['IL'], 1, 0.25)]

TRANSLATE = dict(zip(codons, amino_acids)) 
aa_to_metabolite = dict(zip(amino_acids, all_metabolites))  # Doesn't map final metabolite, JG
aa_to_function = dict(zip(amino_acids, enzyme_functions))
aa_to_reaction = dict(zip(amino_acids, all_reactions))