import os
import biochemistry

class EvolutionaryRun:
    def __init__(self, filename):
        self.generations = 0
        self.metabolites = []
        self.genomes = []
        self.fitnesses = []

        evoFile = file(os.path.join('Genomes', filename), 'r')
        genomes = []
        fitnesses = []

        for line in evoFile:
            if line[0] == '>':
                self.generations += 1
                self.metabolites.append(self._getMetabolites(evoFile.next()))
                if len(genomes) > 0:
                    self.genomes.append(genomes)
                    self.fitnesses.append(fitnesses)
                    genomes = []
                    fitnesses = []

            else:
                temp = line.rstrip('\r').rstrip('\n').split('\t')
                genomes.append(temp[1])
                fitnesses.append(temp[0])

            self.genomes.append(genomes)
            self.fitnesses.append(fitnesses)

    def _getMetabolites(self, metaboliteString):
        metaboliteDictionary = {}

        for metabolite in metaboliteString.split(', ')[:-1]:
            m = metabolite.split(':')
            metaboliteDictionary[m[0]] = float(m[1])

        return metaboliteDictionary

class Genome():
    def __init__ (self, seq, fitness=None):
        self.seq = seq
        self.fitness = fitness
        self.genes = []
        self.proteins = {}
        self.colour = None

    def findGenes(self):
        self.genes = self.seq.split('DDAA')

    def findProteins(self):
        if not self.genes:
            self.findGenes()

        for g in self.genes:
            if len(g) > 3:
                protein = interpretGene(g)

                if protein in self.proteins:
                    self.proteins[protein] += 1
                else:
                    self.proteins[protein] = 1

    def outputProteins(self):
        proteins = self.proteins.keys()
        proteins.sort()

        for p in proteins:
            print self.proteins[p], p

def interpretGene(sequence):
    substrates = []
    products = []
    enz_func = None

    n = 1
    while n < len(sequence):
        codon = sequence[n-1] + sequence[n]

        if enz_func == None:
            if codon in biochemistry.codon_to_function:
                enz_func = biochemistry.codon_to_function[codon]

                if enz_func[0] == 'r':
                    substrates.append('JG')
                    products.append('new protein')
                    enz_func = None

        elif enz_func[0] == 't':
            m = biochemistry.codon_to_metabolite[codon]
            if enz_func[1] == 'f':
                substrates.append('%s out' % m)
                products.append('%s in' % m)
            else:
                substrates.append('%s in' % m)
                products.append('%s out' % m)
            enz_func = None

        elif enz_func[0] == 'e':
            rxn = biochemistry.all_reactions.get(codon, None)

            if rxn:
                if enz_func[1] == 'f':
                    for s in rxn.substrates:
                        substrates.append(s)
                    for p in rxn.products:
                        products.append(p)
                else:
                    for s in rxn.substrates:
                        products.append(s)
                    for p in rxn.products:
                        substrates.append(p)
                enz_func = None

        n += 2

    protein = ''

    if len(substrates) > 0:
        for s in substrates[:-1]:
            protein += '%s + ' % s
        protein += '%s -> ' % substrates[-1]

        for p in products[:-1]:
            protein += '%s + ' % p
        protein += '%s' % products[-1]

    return protein

ancestral_DNA = 'CABCAA-CABCAA-BACC-BACD-BADD-BAADBBBC-BAACBBBA-BCAC-BCAD-BAABBCAA-BCAABDBB'.replace('-', 'DDAA')

e = EvolutionaryRun('Gen 14 genomes.txt')
g = Genome(ancestral_DNA)
g = Genome(e.genomes[0][0])
g.findProteins()
g.outputProteins()

