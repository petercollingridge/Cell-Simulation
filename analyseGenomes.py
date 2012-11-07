import os
import graphDrawer
import biochemistry_old
import numpy as np
from collections import Counter

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

                if protein:
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
            m = biochemistry_old.codon_to_metabolite[codon]
            if enz_func[1] == 'f':
                substrates.append('%s out' % m)
                products.append('%s in' % m)
            else:
                substrates.append('%s in' % m)
                products.append('%s out' % m)
            enz_func = None

        elif enz_func[0] == 'e':
            if codon in biochemistry_old.all_reactions.keys():
                r = biochemistry_old.all_reactions[codon]

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

    # Treat equivalent proteins equally
    substrates.sort()
    products.sort()
    if substrates > products:
        substrates, products = products, substrates

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

def graphNumberOfProteinPerGeneration(proteins_per_generation):
    from drawSVGGraph import Graph

    num_proteins_per_generation = [len(proteins)for proteins in proteins_per_generation]

    g = Graph()
    g.addData({'proteins': num_proteins_per_generation})
    g.x_gridlines = False
    g.plot()
    g.write('test_graph')

def findFirstGenerationForProteins(proteomes_per_generation):
    """ Iteration through list of sets of proteins
        to find the first generation in which each protein appeared. """

    first_generation_for_protein = {}

    for generation, proteome in enumerate(proteomes_per_generation):
        for protein in proteome:
            if protein not in first_generation_for_protein:
                first_generation_for_protein[protein] = generation

    return first_generation_for_protein

def createImageOfProteinsPerGeneration(proteins_per_generation, filtered_proteins):

    import numpy as np
    width = len(proteins_per_generation)
    height = len(filtered_proteins)
    picture = np.zeros((width, height), 'uint64')

    for generation in range(len(proteins_per_generation)):
        for y, protein in enumerate(filtered_proteins):
            if protein in proteins_per_generation[generation]:
                picture[generation, y] = 255

    from imageIO import saveSurface
    saveSurface('test.png', picture)

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

        for n in range(127 - generation):
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

def getMetabolites(filename):
    """ Open file and extract metabolite concentrations for each generation.
        Return a list of dictionaries: list[generation][metabolite] = amount. """

    genomeFile = file(filename, 'r')
    metabolites = []

    for line in genomeFile:
        metaboliteDictionary = {}

        for n in line.split(', ')[:-1]:
            m = n.split(':')
            metaboliteDictionary[m[0]] = float(m[1])
        metabolites.append(metaboliteDictionary)

        for n in range(128):
            genomeFile.next()
    return metabolites

def plotMetabolites():
    # Get metabolites from file of just metabolites
    filename = os.path.join("Genomes", "Gen 1920 metabolites.txt")
    metabolites_per_generation = []

    with open(filename, 'r') as fin:
        for line in fin:
            d = {}
            for metabolites in line.split(', '):
                m, v = metabolites.split(':')
                d[m] = float(v)
            metabolites_per_generation.append(d)

    # Only look at the first 1000 generations
    metabolites_per_generation = metabolites_per_generation[:1000]

    def getMetabolite(m):
        """ Get list of concentrations over the generations for a given metabolite.
            Return as a percentage of the initial concentration and bin into bins of 5. """

        initial_concentration = metabolites_per_generation[0][m]
        return [1000 * (generation[m] - initial_concentration) for generation in metabolites_per_generation]
    

    metabolites_of_interest = ['K', 'F', 'G']
    metabolites_of_interest = ['E', 'H', 'I']
    metabolites_of_interest = ['IL', 'FG', 'FK']
    metabolites_of_interest = ['E', 'H', 'I', 'IL', 'K', 'F', 'G', 'FG', 'FK']
    metabolite_data = {metabolite: getMetabolite(metabolite) for metabolite in metabolites_of_interest}
    for m in metabolites_of_interest:
        print m, metabolite_data[m][-1]

    from drawSVGGraph import Graph


    g = Graph({'height': 300, 'width': 450})
    g.addData(metabolite_data)

    g.x_gridlines = False
    g.colours = ['#3C9DD0', '#034569', '#0C0874']
    g.colours = ['#111'] * 9
    g.addStyle('.gridlines', {'opacity':0.2})
    g.x_axis_label = "Generations"
    g.y_axis_label = "Change in concentration"
    #g.min_y = 0

    g.plot()
    g.write('Conc of E over generations')

def getGenomeArray(filename, start_organism=0, end_organism=128, start_generation=0, end_generation=None):
    """ Returns a 2D array of genomes in which each row contains a list of genomes for a generation
        and each column represents an organism of a given fitness.

        genome_array[10][2] = Genome object for the third fittest organism in generation 10
    """

    genome_array = []
    genomes = []
    generation = 0

    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('EL'):
                generation += 1
                
                if genomes:
                    genome_array.append(genomes)

                genomes = []
                organism = 0

                if generation < start_generation:
                    continue # should actually keep continuing until next EL
                elif end_generation and generation > end_generation:
                    return genome_array
            else:
                if start_organism <= organism < end_organism:
                    temp = line.rstrip().split('\t')
                    genome = Genome(temp[0], temp[1])
                    genome.findProteins()
                    genomes.append(genome)
                    organism += 1

    if genomes:
        genome_array.append(genomes)

    return genome_array

def getProteinCounts(genome_array):
    """ Given a 2D genome array, return a hash of all the proteins and 
        the number of times they occur in the population. """

    protein_counts = Counter()

    for genomes in genome_array:
        for genome in genomes:
            protein_counts.update(genome.proteins)

    return protein_counts

def getProteinCountsPerGenome(genome_array, proteins):
    """ Given a 2D genome_array and a list of proteins, 
        return a 2D array of counts for each protein for each organism. 

        protein_counts[1][3] = counts for protein 4 in organism 2
    """

    protein_counts = np.zeros((0, len(proteins)))

    for genomes in genome_array:
        for genome in genomes:
            counts = np.array([genome.proteins.get(protein, 0) for protein in proteins])
            protein_counts = np.vstack((protein_counts, counts))

    return protein_counts

def PCA(X):
    """ Do principle component analysis on matrix X. """

    m, n = X.shape
    sigma = X.T.dot(X)
    U, S, V = np.linalg.svd(sigma)

    return U, S, V

def displayOrganisms(simple_organisms, n_organisms, n_generations):
    picture = np.zeros((n_generations, n_organisms, 3), 'uint8')

    # Normalise values into the range 0-255
    min_values = np.min(simple_organisms, axis=0)
    max_values = np.max(simple_organisms, axis=0)
    scale = 255 / (max_values - min_values)


    for i in range(len(min_values)):
        simple_organisms[:,i] -= min_values[i]
        simple_organisms[:,i] *= scale[i]

    #Add row of zeros for red colour
    zeros = np.zeros((len(simple_organisms), 1))
    colours = np.hstack((zeros, simple_organisms))

    organism = 0
    for x in range(n_generations):
        for y in range(n_organisms):

            picture[x, y, :] = colours[organism, :]
            organism += 1

    from imageIO import saveSurface
    saveSurface('evolution_pca.png', picture)

def plotEvolutionImage(genome_file, generations, organisms, protein_threshold):
    """ Convert each organism in a given set of generations and of a certain fitness into a colour
        by finding all the proteins that occur more than a certain threshold.
        Then convert each organism into a vector of counts for each protein.
        Use PCA to reduce each organism vector into a vector of two components.
        Then display each organism as a pixel, showing the top organisms over time.
    """

    genome_array = getGenomeArray(genome_file, end_organism=organisms, end_generation=generations)
    protein_counts = getProteinCounts(genome_array)

    filtered_proteins = [protein for protein in protein_counts.iterkeys() if protein_counts[protein] > protein_threshold]
    filtered_proteins.sort(key=lambda x: protein_counts[x], reverse=True)
    print "Found %s proteins occuring above the threshold." % len(filtered_proteins)

    proteins_per_organims = getProteinCountsPerGenome(genome_array, filtered_proteins)
    U, S, V = PCA(proteins_per_organims)
    principle_components = (U[:,:2])
    simple_organism = proteins_per_organims.dot(principle_components)
    displayOrganisms(simple_organism, organisms, generations)

def plotFitness(fitnesses):

    from drawSVGGraph import Graph

    g = Graph({'height': 200, 'width': 500})
    g.addData({'max': [f[0] for f in fitnesses], 'median': [f[63] for f in fitnesses]})

    g.x_gridlines = False
    g.colours = ['#3C9DD0', '#034569', '#0C0874']
    g.addStyle('.gridlines', {'opacity':0.2})
    g.x_axis_label = "Generations"
    g.y_axis_label = "Concentration of IH"
    g.div_x = 480

    g.plot()
    g.write('Fitness over generations')

if __name__ == '__main__':
    genome_file = os.path.join("Genomes", "Gen 1920 genomes.txt")

    genome_array = getGenomeArray(genome_file, end_organism=64, end_generation=200)
    protein_counts = getProteinCounts(genome_array)
    filtered_proteins = [protein for protein in protein_counts.iterkeys() if protein_counts[protein] > 10]
    filtered_proteins.sort(key=lambda x: protein_counts[x], reverse=True)
    print len(protein_counts)
    print len(filtered_proteins)
    print filtered_proteins[0], protein_counts[filtered_proteins[0]]

    #plotEvolutionImage(genome_file, 200, 64, 10)

    # Recover from projection
    # recovered_organisms = simple_organism.dot(principle_components.T)

    #plotMetabolites()

    #fitnesses = getFitnessPerGeneration(genomeFile)
    #plotFitness(fitnesses)

    #with open('results.txt', 'w') as fout:
    #    for name, count in sorted(proteins.iteritems(), key=lambda x: x[1], reverse=True)[:100]:
    #        fout.write("%s\t%d\n" % (name, count))

    #genomes = readGenomes(genomeFile, 1920)
    #for protein, amount in genomes[0].proteins.iteritems():
    #   print protein, amount

    #proteins_per_generation, protein_counts = getProteinCounts(genomeFile, endOrganism=64, max_generations=1900)
    #first_appearance = findFirstGenerationForProteins(proteins_per_generation)
    #graphNumberOfProteinPerGeneration(proteins_per_generation)

    #createImageOfProteinsPerGeneration(proteins_per_generation, filtered_proteins)

