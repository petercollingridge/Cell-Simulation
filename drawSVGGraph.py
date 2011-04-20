import math

#       *** To Do **
#   Get axis divisions work for numbers < 1
#   Get axes to work with data < 1
#   Put SVG elements into a dictionary first
#   Labels data - with mouseover?
#   Allow data to be plotted on two abitrary axes
#   Get text alignments work with different font-sizes?
#   Allow data to have different x values

class Graph:
    def __init__(self):
        self.data = {}
        self.styles = {}
        self.elements = []
        self.colours = ['#0060e5', '#001060', '#e52060', '#a00030', '#00c020', '#006010' ]
        
        self.addStyle('axis', ('stroke','black'), ('stroke-width',0.5))
        self.addStyle('axis-labels', ('font-size','10px'), ('font-family', 'Arial'))
        self.addStyle('data-series', ('stroke-width',1), ('fill',None), ('opacity',0.5))
        self.addStyle('axis-titles', ('font-size','14px'), ('font-family', 'Arial'))
        self.addStyle('gridlines', ('stroke','black'), ('stroke-width', 0.5), ('fill',None), ('opacity',0.5))
        
        self.filter_data = True
        
        self.left_pad  = 50
        self.right_pad = 16
        self.upper_pad = 10
        self.lower_pad = 35
        
        self.x_axis_label = None
        self.y_axis_label = None

    def addDataFromFile(self, filename):
        """ Read in a tab-delimited file with a heading row and add to self.data dictionary """
    
        try:
            fin = open(filename, 'r')
        except IOError:
            print "Could not open file", filename
            return
        
        headings = fin.readline().rstrip('\n').split('\t')
        for h in headings:
            self.data[h] = []
        
        for line in fin.readlines():
            temp = line.rstrip('\n').split('\t')
            for i, h in enumerate(headings):
                self.data[h].append(float(temp[i]))

    def addStyle(self, element, *args):
        """ Add style to self.style dictionary in the form addStyle(element (parameter1, value1), (parameter2, value2)) """
   
        if element not in self.styles:
            self.styles[element] = {}

        for (key, value) in args:
            self.styles[element][key] = value
    
    def _filterData(self, width):
        """ Reduce length of data array to avoid plotting multiple lines per pixel """
        
        filtered_data = {}
        bin = max([len(data) for data in self.data.values()]) / width
        
        for key, data in self.data.items():
            filtered_data[key] = [sum(data[n*bin:(n+1)*bin])*1.0/bin for n in range(len(data)/bin)]
            
        return filtered_data, bin
    
    def _writeStyle(self):
        """ Convert style dictionary into string for SVG """
    
        style_string = '  <style>\n'
      
        for element, style in self.styles.items():
            if ':' not in element:
                style_string += '    .%s{\n' % element
            else:
                style_string += '    %s{\n' % element
            
            for key, value in style.items():
                style_string += '      %s:\t%s;\n' % (key, value)
            style_string += '    }\n'
         
        style_string += '  </style>\n\n'
        
        return style_string

    def outputSVG(self, filename, width=600, height=400):
        if filename[-4:] == '.svg':
            f = file(filename, 'w')
        else:
            f = file("%s.svg" % filename, 'w')
      
        f.write('<?xml version="1.0" standalone="no"?>\n')
        f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
        f.write('<svg width="%d" height="%d" version="1.1" xmlns="http://www.w3.org/2000/svg">\n\n' % (width, height))
        
        if self.styles:
            f.write(self._writeStyle())
        
        f.write('  <rect x="0" y="0" width="%d" height="%d" opacity="0.05"/>\n' % (width, height))
        
        chart_width = width - self.right_pad - self.left_pad
        chart_height = height - self.upper_pad - self.lower_pad
        f.write(self._drawAxis(width, height))
        
        if self.filter_data:
            data, bin = self._filterData(width)
            f.write(self._addDataLines(data, chart_width, chart_height, bin))
        else:
            f.write(self._addDataLines(self.data, chart_width, chart_height))

        f.write('</svg>')
        
    def _drawAxis(self, width, height):
        axis_string = '  <g class="axis">\n'
        axis_string += '    <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>\n' % (self.left_pad-0.5, height-self.lower_pad+0.5, width-self.right_pad-0.5, height-self.lower_pad+0.5)
        #axis_string += '    <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>\n' % (self.left_pad-0.5, height-self.lower_pad+0.5, self.left_pad-0.5, self.upper_pad-0.5)
        axis_string += '  </g>\n'
        
        axis_string += '  <g class="axis-titles">\n'
        if self.x_axis_label:
            axis_string += '    <text x="%.1f" y="%.1f">%s</text>\n' % (width/2, height-self.lower_pad+30, self.x_axis_label)
        if self.y_axis_label:
            axis_string += '    <text x="%.1f" y="%.1f" transform="rotate(270 %.1f %.1f)">%s</text>\n' % (self.left_pad-35, height/2+15, self.left_pad-35, height/2+15, self.y_axis_label)
        axis_string += '  </g>\n'
        
        return axis_string
        
    def _addDataLines(self, data, width, height, bin=1):
        max_y = max([max(d) for d in data.values()])
        max_x = max(len(d) for d in data.values())
        
        div_x = math.pow(10, int(math.log(max_x, 10)))
        if   max_x/div_x > 6: div_x *= 2
        elif max_x/div_x < 4: div_x *= 0.5
        
        div_y = math.pow(10, int(math.log(max_y, 10)))
        if   max_y/div_y > 5: div_y *= 2
        elif max_y/div_y < 3: div_y *= 0.5
        div_y_n = int(math.ceil(max_y/div_y))
        max_y   = div_y_n * div_y
        
        f_x = lambda x: self.left_pad + x*width * 1.0/max_x
        f_y = lambda y: self.upper_pad + height - y*height * 1.0/max_y
        
        path  = ''
        
        #   Gridlines
        path += '  <g class="gridlines">\n'
        for y in range(div_y_n+1):
            gridline_y = int(f_y(y*div_y))+0.5
            path += '    <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>\n' % (self.left_pad, gridline_y, self.left_pad+width, gridline_y)
        path += '  </g>\n'
        
        #   y-axis labels
        path  += '  <g class="axis-labels">\n'
        for y in range(div_y_n+1):
            label_length = y==0 and 3.8 or 3.8*int(math.log(y*div_y, 10)+1)
            if div_y < 1:
                path += '    <text x="%.1f" y="%.1f">%.1f</text>\n' % (self.left_pad-8-label_length, f_y(y*div_y)+3, y*div_y)
            else:
                path += '    <text x="%.1f" y="%.1f">%d</text>\n' % (self.left_pad-8-label_length, f_y(y*div_y)+3, y*div_y)
        
        #   x-axis labels
        x = 0
        while x < max_x:
            label_length = x==0 and 3.2 or 3.2*int(math.log(x*bin,10)+1)
            path += '    <text x="%.1f" y="%.1f">%d</text>\n' % (f_x(x)-label_length, self.upper_pad+height+14, x*bin)
            x += div_x
        path += '  </g>\n'
        
        #   tick marks
        path += '  <g class="axis">\n'
        x = 0
        while x < max_x:
            path += '    <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>\n' % (f_x(x)-0.5, self.upper_pad+height+0.5, f_x(x)-0.5, self.upper_pad+height+4)
            x += div_x
        path += '  </g>\n'
        
        #   Plot lines
        for i, (name, datum) in enumerate(data.items()):
            path += '  <path class="data-series" stroke="%s" d="M%.1f %1f' % (self.colours[i], f_x(0), f_y(datum[0]))
            
            for x, d in enumerate(datum[1:]):
                path += ' L%.1f %1f' % (f_x(x+1), f_y(d))
            path += '"/>\n'
        
        return path
        
if __name__ == '__main__':
    g = Graph()
    g.addDataFromFile('test cell.txt')
    g.x_axis_label = "Time (ms)"
    g.y_axis_label = "Fluorescence"
    
    g.addStyle('axis', ('stroke','black'), ('stroke-width',0.5))
    g.addStyle('axis-labels', ('font-size','10px'), ('font-family', 'Arial'))
    g.addStyle('data-series', ('stroke-width',1), ('fill',None), ('opacity',0.5))
    g.addStyle('axis-titles', ('font-size','14px'), ('font-family', 'Arial'))
    g.addStyle('gridlines', ('stroke','black'), ('stroke-width', 0.5), ('fill',None), ('opacity',0.5))
    g.outputSVG('test')#, width=500, height=300)