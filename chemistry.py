class Chemistry:
    """ Container for all potential chemicals and reactions """
    
    def __init__(self):
        self.chemicals = []
        self.masses = {}
        self.charges = {}
        self.stabilities = {}
        self.reactions = []

    def addElements(self, names, masses, charges):
        for i, name in enumerate(names):
            self.chemicals.append(name)
            self.masses[name] = masses[i]
            self.charges[name] = charges[i]
            self.stabilities[name] = 16 * masses[i] / charges[i] **2
        
    def addMolecules(self, molecules):
        for m in molecules:
            self.chemicals.append(m)
            self.stabilities[m] = self.masses[m[0]] * self.masses[m[1]] * self.charges[m[0]] * self.charges[m[1]]

    def addReaction(self, substrates, products):
        k1 = 2.4 / sum(self.stabilities[s] for s in substrates)
        k2 = 2.4 / sum(self.stabilities[p] for p in products)
        self.reactions.append(Reaction(substrates, products, k1, k2))

class Reaction:
    def __init__(self, substrates, products, k1, k2):
        self.substrates = substrates
        self.products = products
        self.k1 = k1
        self.k2 = k2
        
def defineMetabolitesAndReactions():
    c = Chemistry()
    
    # Define elements
    #elements = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    elements = ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', ]
    masses = [1.0, 2.0, 3.0, 4.0, 2.5, 5.0, 7.5, 10.0]
    charges = [1, 2, 2, 1, 1, 2, 3.2, 1.6]
    c.addElements(elements, masses, charges)

    # Define molecular species
    molecules  = [elements[x*4+y] + elements[z*4-y+3] for x in (0,1) for y in (0,1) for z in (0,1)]
    molecules += [elements[x] + elements[y] for x in (1,5) for y in (1,5)]
    c.addMolecules(molecules)
    
    # Define 12 hydrolysis/synthesis reactions
    for m in molecules:
        c.addReaction([m], [m[0], m[1]])

    # Define 12 transferase reactions
    for x, y in zip((0,2,4,6), (7,6,7,6)):
        c.addReaction([molecules[x], elements[y]], [molecules[x+1], elements[y-4]])
    for x, y in zip((0,1,2,3), (4,4,5,5)):
        c.addReaction([molecules[x], elements[y]], [molecules[x+4], elements[y-4]])
    for x, y in zip((9,10,11,11), (8,8,9,10)):
        c.addReaction([molecules[x], elements[1]], [molecules[y], elements[5]])

    # Define 3 double transferase reactions
    for x, y in [(0,5), (2,7), (8,11)]:
        c.addReaction([molecules[x], molecules[y]], [molecules[x+1], molecules[y-1]])
    
    return elements+molecules, c.reactions