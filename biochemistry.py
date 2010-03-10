class Metabolite:
    def __init__(self, name):
        self.name = name
        self.solutions = {}

class Reaction:
    def __init__(self, substrate_names, product_names, forward_rate, reverse_rate):

        self.substrates = []
        self.products = []
        self.rates = (forward_rate, reverse_rate)

        for s in substrate_names:
            self.substrates.append[all_metabolites[s]]

        for p in product_names:
            self.products.append[all_metabolites[p]]

class Solution():
    def __init__(self, volume):
        self.volume = volume
        self.metabolites = {}

        for metabolite in all_metabolites:
            metabolite.solution[self] = 0.0

class Cell():
    def __init__(self, volume):
        self.volume = volume

class Protein():
    def __init__(self, amount):
        self.amount = amount

# Define all the metabolites and reactions that exist
metabolites = ['ATP', 'ADP', 'Phosphates']
all_metabolites = {}

for m in metabolites:
    all_metabolites[m] = Metabolite[m]

ATPase = Reaction(['ATP', ['ADP', 'Phosphates'], 0.1, 0.0001)
all_reactions = [ATPase]
