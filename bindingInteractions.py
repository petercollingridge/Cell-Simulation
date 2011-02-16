nucleotides = ['A', 'B', 'C', 'D']

class BindingSite:
    def __init__(self, strength, position):
        self.strength = strength
        self.position = position
        self.sequence = None

class AminoAcid:
    def __init__(self, interactions):
        self.interactions = {}
        self.couplets1 = {}
        self.couplets2 = {}

        for nt in range(len(nucleotides)):
            self.interactions[nucleotides[nt]] = int(interactions[nt])

        for nt1, nt2 in [(nt1, nt2) for nt1 in nucleotides for nt2 in nucleotides]:
            self.couplets1[nt1+nt2] = 0.7 * self.interactions[nt1] + 0.3 * self.interactions[nt2]
            self.couplets2[nt1+nt2] = 0.4 * self.interactions[nt1] + 0.6 * self.interactions[nt2]

def findBindingSites(peptide, template):
    sites = []

    if len(peptide) > 3 and len(template) > 5:
        for n in range(0, len(template)-5):
            i1 = amino_acids[peptide[0]].couplets1[template[n:n+2]]
            i2 = amino_acids[peptide[1]].couplets2[template[n+1:n+3]]
            i3 = amino_acids[peptide[2]].couplets1[template[n+3:n+5]]
            i4 = amino_acids[peptide[3]].couplets2[template[n+4:n+6]]
            c1, c2, c3 = i1 + i2, i2 + i3, i3 + i4

            if c1 > 1 and c2 > 1 and c3 > 1:
                sites.append(BindingSite(c1 * c2 * c3, n+6))

    # Sort sites, strongest to weakest
    sites.sort(lambda s1, s2: cmp(s2.strength, s1.strength))

    # Remove competing overlapping sites
    s1 = 0
    while s1 < len(sites):
        s2 = s1 + 1
        while s2 < len(sites):
            # if overlapping
            if sites[s1].position > sites[s2].position-6 and sites[s2].position > sites[s1].position-6:
                #print "(%d-%d; %d) swallows (%d-%d; %d)" % (sites[s1].position-6,  sites[s1].position,  sites[s1].strength,sites[s2].position-6, sites[s2].position, sites[s2].strength)
                sites[s1].strength += 0.5 * sites[s2].strength
                del sites[s2]
            else:
                s2 += 1
        s1 += 1
    return sites

amino_acids = {}
for line in open('aminoAcids.txt'):
    data = line.rstrip('\n').split('\t')
    interactions = data[1].split(',')
    amino_acids[data[0]] = AminoAcid(interactions)