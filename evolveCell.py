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
        if random.random() < 0.995:
            seq += template[n]
        else:
            if random.random() < 0.75:
                seq += random.choice(['A', 'B', 'C', 'D'])
            else:
                n = random.randint(0, len(template)-1)
        n += 1

    return seq

offspring = [12,8,8,8,4,4,4,4,1,1,1,1,1,1,1,1]

def breedCells(cells):
    daughter_DNA = []

    for n in range(16):
        for daughter in range(offspring[n]):
            DNA = mutateSequence(cells[n].DNA)
            daughter_DNA.append(DNA)

    for n in range(4):
        parent = random.randint(0,63)
        DNA = mutateSequence(cells[parent].DNA)
        daughter_DNA.append(DNA)

    return daughter_DNA

ancestral_DNA = 'BACBDDAABACBDDAABAAADDAABAADDDAABCABDDAABABDBCAA'

daughter_DNA = []
for n in range(64):
    DNA = mutateSequence(ancestral_DNA)
    DNA = addRandomSequence(DNA)
    daughter_DNA.append(DNA)

outputFile = file('genome.txt','w')
generation = 0

while True:
    solution = virtualCell.Solution(1000000.0)
    solution.addDefaultMetabolites()
    solution.metabolites['EL'].amount = solution.volume * 0.08
    solution.metabolites['FK'].amount = solution.volume * 0.04

    for n in range(64):
        solution.addCell(1000.0)
        solution.cells[n].addDefaultMetabolites()
        solution.cells[n].DNA = daughter_DNA[n]
        solution.cells[n].interpretDNA()

    for t in range(1000):
        for cell in solution.cells:
            cell.update()

    solution.cells.sort(lambda x, y: cmp(y.metabolites['EH'].amount, x.metabolites['EH'].amount))

    outputFile.write('%s\t%f\n' % (solution.cells[0].DNA, solution.cells[0].metabolites['EH'].amount))
    print "%d, %.4f" % (generation, solution.cells[0].metabolites['EH'].amount)

    daughter_DNA = breedCells(solution.cells)
    generation += 1


