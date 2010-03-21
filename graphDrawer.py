class Graph():
    def __init__ (self):
        self.series = {}
        self.variables = {}
        self.height = 200
        self.width = 400

    def addSeries(self, name):
        self.series[name] = []

    def addDataToSeries(self, series, data):
        self.series[series].append(data)

    def graphSeries(self, series):
        max_values = []

        for s in series:
            max_values.append(max(self.series[s]))
        max_value =  max(max_values)

        print 'Max:', max_value
