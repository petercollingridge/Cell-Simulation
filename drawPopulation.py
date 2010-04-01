class PopulationDiagram():
    def __init__(self, genomes):
        self.genomes = genomes

        self.cols = 8
        self.rows = 16
        self.max_radius = 16

    def findRanges(self):
        fitness = []
        gene_numbers = []

        for g in self.genomes:
            fitness.append(g.fitness)
            gene_numbers.append(len(g.genes))

        self.min_gene_number = min(gene_numbers)
        self.max_gene_number = max(gene_numbers)
        self.gene_number_range = self.max_gene_number - self.min_gene_number
        self.max_fitness = max(fitness)

    def plotPopulation(self):
        self.findRanges()
        self.circles = []

        (x, y) = (self.max_radius, self.max_radius)
        column = 1
        row_height = self.max_radius

        for g in self.genomes:
            size = int(self.max_radius * g.fitness/self.max_fitness)
            if g.colour == None:
                colour = (0, 0, int(255 * (len(g.genes) - self.min_gene_number)/self.gene_number_range))
            else:
                colour = g.colour

            self.circles.append((x, y, size, colour))
            x += self.max_radius*2
            column += 1

            if column > self.cols:
                column = 1
                x = self.max_radius
                y += row_height + size
                row_height = size

    def outputPlot(self, filename):
        (width, height) = (10+self.max_radius*2*8, 10+self.max_radius*2*16)
        svg = open(filename + '.svg', 'w')
        svg.write('<?xml version="1.0" standalone="no"?>\n')
        svg.write("""<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">""")
        svg.write('\n<svg width="%d" height="%d" viewBox="0 0 %d %d"' % (width, height, width, height))
        svg.write(""" 
xmlns="http://www.w3.org/2000/svg" version="1.1">
<style type="text/css" id="style_css_sheet">

.cell {
  opacity: 0.75;
}

.cell:hover {
  opacity: 1;
}

</style>
""")

        for c in self.circles:
            svg.write('<circle class="cell" cx="%d" cy="%d" r="%d" ' % (c[0], c[1], c[2])) 
            svg.write('fill="rgb(%d,%d,%d)" />\n' % (c[3][0], c[3][1], c[3][2]))
        svg.write('</svg>')

