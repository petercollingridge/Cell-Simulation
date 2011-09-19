from chemistry import defineMetabolitesAndReactions

# --- Initialise chemistry ---
CHEMICALS, REACTIONS = defineMetabolitesAndReactions()
default_metabolites = dict([(m, 0.08/2 ** i) for i, m in enumerate(CHEMICALS[:8])])

# Map codons to enzyme functions
NUCLEOTIDES = ['A', 'B', 'C', 'D']
CODONS = [a+b for a in NUCLEOTIDES for b in NUCLEOTIDES]

# --- Define mapping from amino acid sequence to protein function ---
AMINO_ACID_CODE = 'LMNOPQRSTUVWXYZ'
TRANSLATE = dict(zip(CODONS, AMINO_ACID_CODE))
AA_TO_CHEMICAL = dict(zip([a+b for a in AMINO_ACID_CODE[1:] for b in AMINO_ACID_CODE[1:]], CHEMICALS))
AA_TO_REACTION = dict(zip([a+b for a in AMINO_ACID_CODE[1:] for b in AMINO_ACID_CODE[1:]], REACTIONS))

enzyme_functions = 'tf,tr,ef,er,ribosome,binding'.split(',')
aa_to_function = dict(zip(AMINO_ACID_CODE, enzyme_functions))

def Translate(DNA):
    """ Takes a DNA sequence (using nucleotides: A,B,C,D)
        Returns a peptide sequence (using amino acids L-Z) """
        
    peptide = ''
    
    # Splits bases into pairs and cuts off final base if there is an odd number
    for n in range(1, len(DNA), 2):        
        if DNA[n-1:n+1] == 'DD': return peptide
        peptide += TRANSLATE[DNA[n-1:n+1]]
        
    return peptide

class Metabolite:
    def __init__(self, name, volume=100.0):
        self.name = name
        self.volume = volume
        self.amount = 0.0
        
    def concentration(self):
        return 100.0 * self.amount / self.volume

class BindingDomain:
    def __init__(self, sequence):
        self.sequence = sequence
        self.targets = {}
        
    def findPromoterStrengths(self, genes):
        for gene in genes:
            i1 = amino_acids[self.sequence[0]].couplets1[gene.promoter[0:2]]
            i2 = amino_acids[self.sequence[1]].couplets2[gene.promoter[1:3]]
            i3 = amino_acids[self.sequence[2]].couplets1[gene.promoter[3:5]]
            i4 = amino_acids[self.sequence[3]].couplets2[gene.promoter[4:6]]
            c1, c2, c3 = i1 + i2, i2 + i3, i3 + i4
            
            if c1 > 0 and c2 > 0 and c3 > 0:
                self.targets[gene] = [c1 * c2 * c3, 0.0]

class AminoAcid:
    def __init__(self, interactions):
        self.interactions = {}
        self.couplets1 = {}
        self.couplets2 = {}

        for nt in range(len(NUCLEOTIDES)):
            self.interactions[NUCLEOTIDES[nt]] = int(interactions[nt])

        for nt1, nt2 in [(nt1, nt2) for nt1 in NUCLEOTIDES for nt2 in NUCLEOTIDES]:
            self.couplets1[nt1+nt2] = 0.7 * self.interactions[nt1] + 0.3 * self.interactions[nt2]
            self.couplets2[nt1+nt2] = 0.4 * self.interactions[nt1] + 0.6 * self.interactions[nt2]

class Gene:
    def __init__(self, sequence):
        self.promoter = sequence[:6]
        #self.ORF = sequence[6:]
        self.protein_code = Translate(sequence[6:])
        self.occupancy = 0
    
class Protein:
    def __init__(self, sequence, solution):
        self.sequence = sequence
        self.length   = len(sequence)
        self.solution = solution
        
        self.degradation_rate = 0.000004
        self.amount = 0.0
        self.amount_bound = 0.0
        
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
        metabolite  = ''
        
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
            elif domain.startswith('t'):
                if aa == 'L':
                    if metabolite in CHEMICALS:
                        catalytic = True
                        if domain[1] == 'f':
                            self.setMetabolites([metabolite], [metabolite], self.solution.solution)
                        else:
                            self.setMetabolites([metabolite], [metabolite], self.solution, self.solution.solution)
                    domain = None
                    direction = None
                    metabolite = ''
                else:
                    metabolite += AA_TO_CHEMICAL.get(aa, '')
            
            # Enzymes
            elif domain.startswith('e'):
                if aa in AA_TO_REACTION.keys():
                    catalytic = True
                    r = AA_TO_REACTION[aa]
                    
                    if domain[1] == 'f':
                        self.setMetabolites(r.substrates, r.products)
                        self.f_rate *= r.k1
                        self.r_rate *= r.k2
                    else:
                        self.setMetabolites(r.products, r.substrates)
                        self.f_rate *= r.k2
                        self.r_rate *= r.k1
                    domain = None
            
            # Binding Proteins
            elif domain == 'binding':
                if aa == 'L':
                    domain = 'binding sequence'
                    binding_seq = ''
            
            elif domain == 'binding sequence':
                if aa == 'L':
                    if binding_seq and len(binding_seq) >=4 :
                        self.binding_domains.append(BindingDomain(binding_seq))
                    domain = None
                else:
                    binding_seq += aa
            
        if self.binding_domains:
            self.functions.append(self.bind)
        if ribosome:
            self.functions.extend([self.find_reaction_rate, self.translate])
        elif catalytic:
            self.functions.extend([self.find_reaction_rate, self.catalyse])
        
        for domain in self.binding_domains:
            domain.findPromoterStrengths(self.solution.genes)

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
            for gene, (strength, tmp) in site.targets.items():
                print "Binds sequence %s with strength %0.2f" % (gene.promoter, strength)

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
        
        self.net_rxn = substrate_bound - product_bound

    def catalyse(self):
        self.net_rxn *= self.amount
        for s in self.substrates:
            s.amount -= self.net_rxn
        for p in self.products:
            p.amount += self.net_rxn

    def bind(self):
        free_protein = self.amount - self.amount_bound
        
        for domain in self.binding_domains:
            for gene, (strength, amount_bound) in domain.targets.items():
                association  = ((1.0-gene.occupancy)/len(self.solution.genes))*free_protein/(free_protein*len(self.binding_domains)+1.0)
                association -= (amount_bound+association) * 1.0 / (strength + 1.0)
                gene.occupancy += association
                domain.targets[gene][1] += association
                self.amount_bound += association             
                      
        #print "amount bound", self.amount_bound

    def translate(self):
        if self.net_rxn > 0 and self.amount_bound > 0:
            for domain in self.binding_domains:
                for gene, (strength, amount_bound) in domain.targets.items():
                    self.solution.addProtein(gene.protein_code, self.net_rxn *amount_bound/len(gene.protein_code))
            
            self.net_rxn *= self.amount_bound
            for s in self.substrates:
                s.amount -= self.net_rxn
            for p in self.products:
                p.amount += self.net_rxn

    def update(self):
        for function in self.functions:
            function()

# Define amino acids for their interactions

amino_acids = {}
for line in open('aminoAcids.txt'):
    data = line.rstrip('\n').split('\t')
    interactions = data[1].split(',')
    amino_acids[data[0]] = AminoAcid(interactions)