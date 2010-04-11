import graphDrawer
import biochemistry
import drawPopulation

class Genome():
    def __init__ (self, seq, fitness):
        self.seq = seq
        self.fitness = fitness
        self.genes = seq.split('DDAA')
        self.proteins = {}
        self.colour = None

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
    differences = [0]

    for p in p1.keys():
        if p in p2:
            if p1[p] > p2[p]:
                differences.append('Lost %d copies of %s' % (p1[p]-p2[p], p))
                differences[0] += p1[p]-p2[p]
            if p1[p] < p2[p]:
                differences.append('Gained %d copies of %s' % (p2[p]-p1[p], p))
                differences[0] += p2[p]-p1[p]
        else:
            differences.append('Lost %d copies of %s' % (p1[p], p))
            differences[0] += p1[p]

    for p in p2.keys():
        if p not in p1:
            differences.append('New protein %s' % p)
            differences[0] += p2[p]

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

def readGenomes(filename):
    # Old style genomes with each line having 'genome' <tab> 'fitness'

    genomeFile = file(filename, 'r')
    genomes = []

    for line in genomeFile.readlines():
        temp = line.split('\t')
        g = Genome(temp[0], float(temp[1]))
        g.findProteins()
        genomes.append(g)

        graph.addDataToSeries('[EH]', g.fitness)
        graph.addDataToSeries('genes', len(g.genes))

    return genomes

def readGenomes2(filename, target_generation):
    genomeFile = file(filename, 'r')
    genomes = []
    generation = 0

    for line in genomeFile:
        metabolites = line

        if generation == target_generation:
            for n in range(128):
                data = genomeFile.next()
                temp = data.rstrip('\r\n').split('\t')

                g = Genome(temp[0], float(temp[1]))
                g.findProteins()
                genomes.append(g)
        else:
            for n in range(128):
                genomeFile.next()
        generation += 1

    return genomes

def filterGenomeByFitnessPosition(filename, position):
    genomeFile = file(filename, 'r')
    genomes = []

    for line in genomeFile:
        metabolites = line

        for n in range(generation):
            genomeFile.next()

        data = genomeFile.next()
        temp = data.rstrip('\r\n').split('\t')

        g = Genome(temp[0], float(temp[1]))
        g.findProteins()
        genomes.append(g)

        for n in range(127-generation):
            genomeFile.next()

    return genomes

def colourByDistance(genomes):
    distance_matrix = {}

    for i in range(len(genomes)):
        for j in range(i+1, len(genomes)):
            d = compareProteomes(genomes[i], genomes[j])
            distance_matrix[(i, j)] = d[0]
            distance_matrix[(j, i)] = d[0]

    max_distance  = max(distance_matrix.values())

    for i in distance_matrix.keys():
        if distance_matrix[i] == max_distance:
            (g1, g2) = i
            break

    for n in range(len(genomes)):
        if n != g1:
            d1 = int(255 * distance_matrix[(n, g1)] / max_distance)
        else:
            d1 = 0

        if n != g2:
            d2 = int(255 * distance_matrix[(n, g2)] / max_distance)
        else:
            d2 = 0

        genomes[n].colour = (0, d1, d2)

    return genomes

def createProteinDistanceMatrix(genomes):
    total_distance = 0

    for i in range(len(genomes)):
        for j in range(i+1, len(genomes)):
            d = compareProteomes(genomes[i], genomes[j])
            total_distance += d[0]

    print total_distance

def PlotPop(genomes):
    genomes = []
    for g in range(16):
        g = readGenomes2(genomeFile, g)
        genomes.extend(g[:16])
    genomes = colourByDistance(genomes)

    pd = drawPopulation.PopulationDiagram(genomes)
    pd.plotPopulation()
    pd.outputPlot('test circles')

genomeFile = 'Genomes/Gen 1920 genomes.txt'

graph = graphDrawer.Graph()
graph.addSeries(name = '[IH]')
graph.addSeries(name = 'genes')

#PlotPop(genomes)
genomes = filterGenomeByFitnessPosition(genomeFile, position=64)

for g in genomes:
    graph.addDataToSeries('[IH]', g.fitness)
    graph.addDataToSeries('genes', len(g.genes))

graph.X_axis.tick_number = 4
graph.outputSeries('Run2 Gen1920 fitness Gen0', ['[IH]', 'genes'], X_range=(0,1920))

#for n in range(25):
#    print n,
#    genomes = readGenomes2(genomeFile, n)
#    createProteinDistanceMatrix(genomes)

#outputGenomeDifferences(genomes)

#genomes[0].outputProteins()

