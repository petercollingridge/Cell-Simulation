import virtualCell
import random

def addRandomSequence(seq):
    while random.random() < 0.99:
        seq += random.choice(['A', 'B', 'C', 'D'])
    return seq

def copySequenceWithErrors(template):
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

def breedCells(cells):
    offspring = [12,8,8,8,4,4,4,4,1,1,1,1,1,1,1,1]
    daughter_DNA = []

    for n in range(len(offpring)):
        for daughter in range(offspring[n]):
            daughter_DNA.append(copySequenceWithErrors(cells[n].DNA))

    for n in range(4):
        parent = random.randint(0, NUMBER_OF_CELLS-1)
        daughter_DNA.append(copySequenceWithErrors(cells[parent].DNA))

    return daughter_DNA

def outputGeneration(generation, solution):
    outputFile.write('>Generation %d\n' % generation)

    for m in solution.metabolites.keys():
        outputFile.write('%s:%f, ' % (m, solution.metabolites[m].concentration()))
    outputFile.write('\n')

    for cell in solution.cells:
        outputFile.write('%f\t%s\n' % (cell.metabolites['EH'].amount, cell.DNA[0]))

    print "Generation: %d, Genes: %d, Fitness: %.4f" % (generation, len(solution.cells[0].proteins.keys()), solution.cells[0].metabolites['EH'].amount)

#   Define metabolites in pool
solution_metabolites = virtualCell.default_metabolites
solution_metabolites['FK'] = 0.20
solution_metabolites['IL'] = 0.08
solution_metabolites['FG'] = 0.08
solution_metabolites['JG'] = 0.04
solution_metabolites['EL'] = 0.01

#   Create generation 0
GENERATION_TIME = 48000
NUM_GENERATIONS = 10
NUMBER_OF_CELLS = 64
SOLUTION_VOLUME = 2000000.0
CELL_VOLUME = 1000.0
outputFile = file('110525 genomes.txt','w')

ancestral_DNA  = 'AAAAAD BB AA BBBBBBBA AA BA ACAA DDAAAA'    # Transcription factor
ancestral_DNA += 'AADAAD AA ACADAA DDAAAA'                    # FG pore
ancestral_DNA += 'AADAAD AA ACBDAA DDAAAA'                    # FK pore
ancestral_DNA += 'AADAAD AA BCADAA DDAAAA'                    # JG pore
ancestral_DNA += 'AADAAD AA ADAA AB BBAA DDAAAA'              # G/I antiporter
ancestral_DNA += 'AADAAD AA BAAA AB BDAA DDAAAA'              # H/K antiporter
ancestral_DNA += 'AADAAD AC AC DDAAAA'                        # FGase
ancestral_DNA += 'AADAAD AC AD DDAAAA'                        # FKase
ancestral_DNA += 'AADAAD AA ACAA AC AA DDAAAA'                # F-driven EHase
ancestral_metabolites = {'E':0.8, 'F':0.4, 'G':0.2, 'H':0.1, 'I':0.05, 'J':0.025, 'K':0.0125, 'L':0.00625}

daughter_DNA = [addRandomSequence(copySequenceWithErrors(ancestral_DNA)) for n in range(NUMBER_OF_CELLS)]
daughter_metabolites = []

for generation in range(NUM_GENERATIONS):
    solution = virtualCell.Solution(SOLUTION_VOLUME, solution_metabolites)

    # Create cells
    for n in range(NUMBER_OF_CELLS):
        cell = solution.addCell(CELL_VOLUME)
        cell.addDNA(daughter_DNA[n])

        for p in cell.proteins.values():
            p.amount = 1

    # Run Simulation
    for t in range(GENERATION_TIME):
        for cell in solution.cells:
            cell.update()

    solution.cells.sort(lambda x, y: cmp(y.metabolites['EH'].amount, x.metabolites['EH'].amount))
    outputGeneration(generation, solution)
    
    # Takes the genomes from first half of a list of cells and mutates each twice, returning a list of those genomes
    # Therefore every cell in the top 50% gets to replicate
    daughter_DNA = [copySequenceWithErrors(solution.cells[int(n/2)].DNA) for n in range(NUMBER_OF_CELLS)]