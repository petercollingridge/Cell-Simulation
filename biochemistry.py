class Reaction:
    def __init__(self, substrates, products, forward_rate, reverse_rate):

        self.substrates = substrates
        self.products = products
        self.rates = (forward_rate, reverse_rate)

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
all_metabolites = ['ATP', 'ADP', 'Phosphates']

ATPase = Reaction(['ATP', ['ADP', 'Phosphates'], 0.1, 0.0001)
all_reactions = [ATPase]
