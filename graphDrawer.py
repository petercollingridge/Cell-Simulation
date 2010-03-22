class Graph():
    def __init__ (self):
        self.series = {}
        self.variables = {}
        self.border = (40, 5, 75, 40)
        self.scaleX = 1.0
        self.scaleY = 1.0
        self.colours = ['#0060e5', '#001060', '#e52060', '#a00030', '#00c020', '#006010' ]

        self.X_axis = Axis(360)
        self.Y_axis = Axis(200)

    def addSeries(self, name):
        n = len(self.series.keys())
        newSeries = DataSeries(name, n)
        self.series[name] = newSeries

    def addDataToSeries(self, name, data):
        self.series[name].data.append(data)

    def outputSeries(self, filename, series):
        self.initiliseSVG(filename)
 
        X_values = []
        Y_values = []
        for s in series:
            X_values.append(len(self.series[s].data))
            Y_values.append(max(self.series[s].data))

        max_X = max(X_values)
        max_Y = max(Y_values)
        self.scaleX = 1.0 * self.X_axis.length / max_X
        self.scaleY = 1.0 * self.Y_axis.length / max_Y

        self.X_axis.range = (0, max_X)
        self.Y_axis.range = (0, max_Y)
        self.X_axis.tick_interval = self.X_axis.range[1] / 5
        self.Y_axis.tick_interval = 10

        self.X_axis.drawX(self.svg, self.border[0], self.Y_axis.length + self.border[1], self.scaleX)
        self.Y_axis.drawY(self.svg, self.border[0], self.Y_axis.length + self.border[1], self.scaleY)

        for s in series:
            self.drawPlot(self.series[s])

        self.drawLabels()
        self.svg.write('</svg>')

    def initiliseSVG(self, name):
        width  = self.X_axis.length + self.border[0] + self.border[2] 
        height = self.Y_axis.length + self.border[1] + self.border[3] 

        self.svg = open(name + '.svg', 'w')
        self.svg.write('<?xml version="1.0" standalone="no"?>\n')
        self.svg.write("""<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">""")
        self.svg.write('\n<svg width="%d" height="%d" viewBox="0 0 %d %d"' % (width, height, width, height))
        self.svg.write(""" 
xmlns="http://www.w3.org/2000/svg" version="1.1">
<style type="text/css" id="style_css_sheet">

.axis {
  fill-opacity: 0;
  stroke: black;
  stroke-width: 1;
  stroke-opacity: 1;
}

.axis_text {
  font-size: 12px;
  fill: black;
}

.axis_label {
  font-size: 16px;
  fill: black;
}

.data {
  fill-opacity: 0;
  stroke: #989898;
  stroke-opacity:0.8;
  stroke-width: 3;
}

.label {
  stroke-width: 0;  
  font-size: 16px;
  fill: black;
  opacity: 0.4;
}

.label:hover {
  opacity: 0.9;
}

</style>
""")

    def drawPlot(self, series):
        dx = self.border[0]
        dy = self.border[1] + self.Y_axis.length

        self.svg.write('<path class="data" visibility="hidden" ')
    #    self.svg.write('stroke="%s" ' % series.colour)

        for n in range(len(series.data)):
            x = n * self.scaleX + dx
            y = dy - series.data[n] * self.scaleY

            if n > 0:
                self.svg.write('L%d, %.3f ' % (x, y))
            else:
                self.svg.write('d="M%d, %.3f ' % (x, y))

        self.svg.write('">\n')
        self.svg.write('<set attributeName="visibility" from="hidden" to="visible" ')
        self.svg.write('begin="label%d.mouseover" end="label%d.mouseout"></set>\n' % (series.number, series.number))
        self.svg.write('</path>\n')

    def drawLabels(self):
        x = self.border[0] + self.X_axis.length + 10
        y = self.border[1] + 20

        series = self.series.keys()
        series.sort()

        for s in series:
            self.svg.write('<text id="label%d" class="label" x="%d" y="%d" ' % (self.series[s].number, x, y))
            self.svg.write('fill="%s">%s</text>\n' % (self.series[s].colour, self.series[s].label))
            y += self.Y_axis.length / len(self.series)

    def writeFinalValue(self, series):
        pass

class DataSeries():
    def __init__(self, label, number):
        self.colour = '#000000'
        self.number = number
        self.label = label
        self.data = []

class Axis():
    def __init__(self, length):
        self.length = length
        self.range = (0, 1) 
        self.tick_interval = 0.2

    def drawX(self, svg, x, y, dx):
        if self.tick_interval * dx == 0: return

        svg.write(' <path class="axis" d="M%d, %d L%d, %d" />\n' % (x, y, x+self.length, y))
        svg.write(' <text class="axis_label" x="%d" y="%d">Time</text>\n' % (x+self.length/2-20, y+40))

        label = self.range[0]
        while label <= self.range[1]:
            svg.write(' <path class="axis" d="M%d %d L%d %d" />\n' % (x, y-0.5, x, y+8))
            labelX = x - len(str(label))*4
            svg.write(' <text class="axis_text" x="%d" y="%d" >%s</text>\n' % (labelX, y+20, label))

            x += self.tick_interval * dx
            label += self.tick_interval

    def drawY(self, svg, x, y, dy):
        if self.tick_interval * dy == 0: return

        svg.write(' <path class="axis" d="M%d, %d L%d, %d" />\n' % (x, y, x, y-self.length))

        label = self.range[0]
        while label <= self.range[1]:
            svg.write(' <path class="axis" d="M%d %d L%d %d" />\n' % (x-8, y, x+0.5, y))
            labelX = x - 10 - len("%.1f" % label)*7
            svg.write(' <text class="axis_text" x="%d" y="%d" >%.0f%%</text>\n' % (labelX, y+4, label))

            y -= self.tick_interval * dy
            label += self.tick_interval

