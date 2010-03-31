import virtualCell
import random

def addRandomSequence(seq):
    while random.random() < 0.995:
        seq += random.choice(['A', 'B', 'C', 'D'])

    return seq

def mutateSequence(template):
    seq = ''
    n = 0

    while n < len(template):
        if random.random() < 0.999:
            seq += template[n]
        else:
            if random.random() < 0.75:
                seq += random.choice(['A', 'B', 'C', 'D'])
            else:
                n = random.randint(0, len(template)-1)
        n += 1

    return seq

def addCell(seq):
    solution.addCell(1000.0)
    solution.cells[-1].addDefaultMetabolites()
    solution.cells[-1].DNA = seq
    solution.cells[-1].interpretDNA()

def breedCells(cells):
    offspring = [12,8,8,8,4,4,4,4,1,1,1,1,1,1,1,1]
    daughter_DNA = []

    for n in range(len(offpring)):
        for daughter in range(offspring[n]):
            DNA = mutateSequence(cells[n].DNA)
            daughter_DNA.append(DNA)

    for n in range(4):
        parent = random.randint(0,number_of_cells-1)
        DNA = mutateSequence(cells[parent].DNA)
        daughter_DNA.append(DNA)

    return daughter_DNA

def doubleCells(cells):
    daughter_DNA = []

    for n in range(number_of_cells/2):
        for daughters in range(2):
            DNA = mutateSequence(cells[n].DNA)
            daughter_DNA.append(DNA)

    return daughter_DNA

def outputGeneration(generation, solution):
    outputFile.write('>Generation %d\n' % generation)

    solution.cells.sort(lambda x, y: cmp(y.metabolites['IH'].amount, x.metabolites['IH'].amount))
    for m in solution.metabolites.keys():
        outputFile.write('%s:%f, ' % (m, solution.metabolites[m].amount/solution.volume))
    outputFile.write('\n')

    for cell in solution.cells:
        outputFile.write('%f\t%s\n' % (cell.metabolites['IH'].amount, cell.DNA))

    print "Generation: %d, Genes: %d, Fitness: %.4f" % (generation, len(solution.cells[0].proteins.keys()), solution.cells[0].metabolites['IH'].amount)

#   Define metabolites in pool
defaultMetabolites = virtualCell.defaultMetabolites
defaultMetabolites['FK'] = 1.6 / 10.0
defaultMetabolites['IL'] = 0.8 / 10.0
defaultMetabolites['FG'] = 0.6 / 10.0
defaultMetabolites['JG'] = 0.4 / 10.0
defaultMetabolites['EL'] = 0.1 / 10.0

#   Create generation 0
number_of_cells = 128
generation_time = 10

ancestral_DNA = 'CABCAA-CABCAA-BACC-BACD-BADD-BAADBBBC-BAACBBBA-BCAC-BCAD-BAABBCAA-BCAABDBB'.replace('-', 'DDAA')
ancestral_metabolites = {'E':0.8, 'F':0.4, 'G':0.2, 'H':0.1, 'I':0.05, 'J':0.025, 'K':0.0125, 'L':0.00625}

daughter_DNA = []
daughter_metabolites = []

for n in range(number_of_cells):
    DNA = mutateSequence(ancestral_DNA)
    DNA = addRandomSequence(DNA)
    daughter_DNA.append(DNA)

outputFile = file('genomes.txt','w')
generation = 0

while True:
    solution = virtualCell.Solution(2000000.0)
    solution.setMetabolites(defaultMetabolites)

    for n in range(number_of_cells):
        solution.addCell(1000.0)
        solution.cells[n].setMetabolites('default')
        solution.cells[n].DNA = daughter_DNA[n]
        solution.cells[n].interpretDNA()

        for p in solution.cells[-1].proteins.values():
            p.amount = 1

    for t in range(generation_time):
        for cell in solution.cells:
            cell.update()

    outputGeneration(generation, solution)
    daughter_DNA = doubleCells(solution.cells)
    generation += 1
