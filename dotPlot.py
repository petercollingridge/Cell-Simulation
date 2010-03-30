def initiliseSVG(filename, (width, height)):
    svg = open(filename + '.svg', 'w')
    svg.write('<?xml version="1.0" standalone="no"?>\n')
    svg.write("""<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">""")
    svg.write('\n<svg width="%d" height="%d" viewBox="0 0 %d %d"' % (width, height, width, height))

    svg.write(""" 
xmlns="http://www.w3.org/2000/svg" version="1.1">
<style type="text/css" id="style_css_sheet">

.dot {
  fill-opacity: 1;
}

.dot_line {
  fill-opacity: 0;
  stroke: #101010;
  stroke-width: 1.5;
  stroke-opacity: 1;
}

</style>
""")

    return svg

def plot_dot_plot(DNA, dot_colours=None):
    for i in range(num_NTs):
        for j in range(i, num_NTs):

            if DNA[i] == DNA[j]:
                svg.write('<circle class="dot" cx="%d" cy="%d" r="1" ' % (i*2+1, j*2+1))

                if dot_colours != None:
                    svg.write('fill="%s"/>\n' % dot_colours[DNA[i]])
                else:
                    svg.write('/>\n')
    svg.write('</svg>')

def plot_dot_lines(DNA):
    for i in range(num_NTs-2):
        line_length = 0

        for j in range(1, num_NTs-i):
            if DNA[j] == DNA[j+i]:
                line_length += 1
            else:
                if line_length > 5:
                    print i, j, line_length
                    (x, y) = (scale * (j-line_length), scale * (j+i-line_length))
                    svg.write('<path class="dot_line" d="M%d %d L%d %d" />\n' % (scale*j, scale*(j+i), x, y))
                line_length = 0
    svg.write('</svg>')

DNA = 'BACBCCDBCBCAADADDAABABDBBADDCCAAADADBACCBCADCCDDAABCABDDAABABDBCAACCACACABDCAADDAABABDBBADCBDDDAABACBCCDBCBCAADADDAABABDBBADDADDABADCABCBDDAABCABDDAABABDBCAADDCDCDDDDAABABDBBADBACDDAABACBCCDBCBCAADADDAABABDBBADDACDAADBAAAADDDAABCABDDAABABDBCAAAAACCDCABDDAABABDBCAAADDDDDABCCAACBADCDADDAABABDBBADCBCDDAABABDBBADDCDABBDDAABABDBCAAACACCDCCDCBAB'
num_NTs = len(DNA)
scale = 1

svg = initiliseSVG('test', (scale*num_NTs+2, scale*num_NTs+2))
dot_colours = {'A': 'red', 'B': 'blue', 'C': 'green', 'D': 'black'}

#plot_dot_plot(DNA)
plot_dot_lines(DNA)
