class Graph():
    def __init__ (self):
        self.series = {}
        self.variables = {}
        self.height = 400
        self.width = 400
        self.border = 20
        self.axis_border = 40
        self.scaleX = 1.0
        self.scaleY = 1.0
        self.colours = ['#c00000', '#00c000', '#0000c0', '#c0c000', '#c000c0']

    def addSeries(self, name):
        newSeries = DataSeries(name)
        newSeries.colour = self.colours[len(self.series.keys())]
        self.series[name] = newSeries

    def addDataToSeries(self, name, data):
        self.series[name].data.append(data)

    def outputSeries(self, filename, series):
        self.initiliseSVG(filename)

        max_values = []
        plots = {}

        for s in series:
            max_values.append(max(self.series[s].data))
            plots[s] = []
        max_value =  max(max_values)

        self.scaleX = 1.0 * self.width / len(self.series[series[0]].data)
        self.scaleY = 1.0 * self.height / max_value

        for s in series:
            self.drawPlot(self.series[s])

        x = self.axis_border + self.border
        for s in series:
            self.drawLabel(self.series[s], x, 20)
            x += self.width / len(series)
    
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
        self.svg.write('\n.data{\n  fill-opacity: 0;\n stroke-opacity:0.7;\n  stroke-width: 1.5;\n}')
        self.svg.write('\n </style>\n')
        self.svg.write('<path class="axis" d="M%d, %d L%d, %d L%d %d" />\n' % (dx, self.border, dx, dy, self.width+self.axis_border+self.border, dy))

    def drawPlot(self, series):
        dx = self.border+self.axis_border
        dy = self.height+self.border

        self.svg.write('<path class="data" stroke="%s" ' % series.colour)

        for n in range(len (series.data)-1):
            x = n * self.scaleX + dx
            y = dy - series.data[n] * self.scaleY

            if n > 0:
                self.svg.write('L%d, %.3f ' % (x, y))
            else:
                self.svg.write('d="M%d, %.3f ' % (x, y))

        self.svg.write('" />\n')

    def drawLabel(self, series, x, y):
        self.svg.write('<text x="%d" y="%d" fill="%s">%s</text>\n' % (x, y, series.colour, series.label))

class DataSeries():
    def __init__(self, label):
        self.label = label
        self.data = []
        self.colour = '#000000'        
