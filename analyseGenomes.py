import graphDrawer
import biochemistry

genomeFile = file('Genomes/Gen2810 genomes.txt', 'r')

class Genome():
    def __init__ (self, seq, fitness):
        self.seq = seq
        self.fitness = fitness
        self.genes = seq.split('DDAA')
        self.proteins = {}

    def findProteins(self):
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
            if codon == 'BA':
                enz_func = 'tf'
            elif codon == 'BB':
                enz_func = 'tr'
            if codon == 'BC':
                enz_func = 'ef'
            elif codon == 'BD':
                enz_func = 'er'

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
            if codon in biochemistry.all_reactions.keys():
                r = biochemistry.all_reactions[codon]

                if enz_func[1] == 'f':
                    for s in r.substrates:
                        substrates.append(s)
                    for p in r.products:
                        products.append(p)
                else:
                    for s in r.substrates:
                        products.append(s)
                    for p in r.products:
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

def compareProteomes(genome1, genome2):
    p1 = genome1.proteins
    p2 = genome2.proteins
    differences = []

    for p in p1.keys():
        if p in p2:
            if p1[p] > p2[p]:
                differences.append('Lost %d copies of %s' % (p1[p]-p2[p], p))
            if p1[p] < p2[p]:
                differences.append('Gained %d copies of %s' % (p2[p]-p1[p], p))
        else:
            differences.append('Lost %d copies of %s' % (p1[p], p))

    for p in p2.keys():
        if p not in p1:
            differences.append('New protein %s' % p)

    return differences

def outputGenomeDifferences(genomes):
    for n in range(1, len(genomes)):
        if genomes[n-1].seq != genomes[n].seq:
            differences = compareProteomes(genomes[n-1], genomes[n])

            if len(differences) > 0:
                print '>Generation %d, %f' % (n, genomes[n].fitness)
                print ' %d nts, %d genes' % (len(genomes[n].seq), len(genomes[n].genes))

                for d in differences:
                    print ' ', d

graph = graphDrawer.Graph()
graph.addSeries(name = '[EH]')
graph.addSeries(name = 'genes')

genomes = []
for line in genomeFile.readlines():
    temp = line.split('\t')
    g = Genome(temp[0], float(temp[1]))
    g.findProteins()
    genomes.append(g)

    graph.addDataToSeries('[EH]', g.fitness)
    graph.addDataToSeries('genes', len(g.genes))

outputGenomeDifferences(genomes)
#genomes[0].outputProteins()

#graph.X_axis.tick_number = 7
graph.outputSeries('gene graph2', ['[EH]','genes'], X_range=(0,300))
