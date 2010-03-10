class Metabolite:
    def __init__(self, name):
        self.name = name
	self.solutions = {}

class Reaction:
    def __init__(self, substrates, products, forward_rate, reverse_rate):
        self.chemicals = (substrates, products)
        self.rates = (forward_rate, reverse_rate)

class Solution:
    def __init__(self, volume):
	self.volume = volume

ATP = Metabolite('ATP')
ADP = Metabolite('ADP')
Pi  = Metabolite('Phosphates')
ATPase = Reaction([ATP], [ADP, Pi], 0.1, 0.0001)

all_metabolites = [ATP, ADP, Pi]
all_reactions = [ATPase]
