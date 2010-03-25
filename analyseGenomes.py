import graphDrawer
import biochemistry

genomeFile = file('Gen2810 genomes.txt', 'r')

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

    for s in substrates[:-1]:
        protein += '%s + ' % s
    protein += '%s -> ' % substrates[-1]

    for p in products[:-1]:
        protein += '%s + ' % p
    protein += '%s' % products[-1]

    return protein

class Genome():
    def __init__ (self, seq, fitness):
        self.seq = seq
        self.fitness = fitness
        self.genes = seq.split('DDAA')
        self.proteins = {}

    def findProteins(self):
        for g in self.genes:
            protein = interpretGene(g)

            if protein in self.proteins:
                self.proteins[protein] += 1
            else:
                self.proteins[protein] = 1

genomes = []
for line in genomeFile.readlines():
    temp = line.split('\t')
    g = Genome(temp[0], float(temp[1]))
    genomes.append(g)


for n in range(1, len(genomes)):
    if genomes[n-1].seq != genomes[n].seq:
        pass
#        print "%d:\t%d" % (n, len(genomes[n].seq))

target_genome = -1

genomes[target_genome].findProteins()
proteins = genomes[target_genome].proteins.keys()
proteins.sort()

for p in proteins:
    print genomes[target_genome].proteins[p], p
