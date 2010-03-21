class Graph():
    def __init__ (self):
        self.series = {}
        self.variables = {}
        self.height = 400
        self.width = 400
        self.border = 10
        self.axis_border = 50

    def addSeries(self, name):
        self.series[name] = []

    def addDataToSeries(self, series, data):
        self.series[series].append(data)

    def outputSeries(self, filename, series):
        self.initiliseSVG(filename)

        max_values = []
        plots = {}

        for s in series:
            max_values.append(max(self.series[s]))
            plots[s] = []
        max_value =  max(max_values)

        dx = 1.0*len(self.series[series[0]]) / self.width
        dy = self.height / max_value

        for n in range(self.width):
            x = int(n*dx)
            for s in series:
                plots[s].append((n, dy * self.series[s][x]))
            x += dx

        for s in series:
            self.drawPlot(plots[s])
        self.svg.write('</svg>')

    def initiliseSVG(self, name):
        width  = self.width  + self.border*2 + self.axis_border
        height = self.height + self.border*2 + self.axis_border
        dx = self.border+self.axis_border
        dy = self.height+self.border

        self.svg = open(name + '.svg', 'w')
        self.svg.write('<?xml version="1.0" standalone="no"?>\n')
        self.svg.write("""<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">""")
        self.svg.write('\n<svg width="%d" height="%d" viewBox="0 0 %d %d"\n' % (width, height, width, height))
        self.svg.write('xmlns="http://www.w3.org/2000/svg" version="1.1">\n')

        self.svg.write(' <style type="text/css" id="style_css_sheet">\n')
        self.svg.write('\n.axis{\n  fill-opacity: 0;\n  stroke: black;\n  stroke-opacity:1;\n  stroke-width: 2;\n}')
        self.svg.write('\n.data{\n  fill-opacity: 0;\n  stroke: blue;\n  stroke-opacity:0.8;\n  stroke-width: 1;\n}')
        self.svg.write('\n </style>\n')
        self.svg.write('<path class="axis" d="M%d, %d L%d, %d L%d %d" />\n' % (dx, self.border, dx, dy, self.width+self.axis_border+self.border, dy))

    def drawPlot(self, coordinates):
        dx = self.border+self.axis_border
        dy = self.height+self.border

        self.svg.write('<path class="data" d="M')

        for (x, y) in coordinates[:-1]:
            self.svg.write('%d, %.3f L' % (x+dx, dy-y))

        self.svg.write('%d, %.3f" />\n' % (coordinates[-1][0]+dx, dy-coordinates[-1][1]))
        
