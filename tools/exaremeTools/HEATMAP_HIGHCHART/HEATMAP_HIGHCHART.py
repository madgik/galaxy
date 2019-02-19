import requests
import json
import sys

endpoint='http://88.197.53.100:9090'


def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
            argv = argv[2:]
        else:
            argv = argv[1:]
    return opts
	
def main():
	args = sys.argv[1:]

	opts = getopts(args)
		
	if not opts or len(opts) < 2:
		print("Usage:")
		print(" -in Input")
		print(" -o Output")
		return 0
		
	try:
		inputFile = open(opts.get("-in"), "r")
		inputData = inputFile.read()
		inputJson = json.loads(inputData)
		title = 'Confusion Matrix'
		xtitle = 'Actual class'
		ytitle = 'Predicted class'
		results = inputJson['results']
	except ValueError:
		print("Input file should be:")
		print("{")
		print('  "results" : [ ... ]')
		print("}")
	
	highcharts = []
	for result in results:
		highcharts.append(heatmap(result,title,xtitle,ytitle))
	
	outputJson = {"highcharts" : highcharts}
	
	outputFile = open(opts.get("-o"), "w")
	outputFile.write(json.dumps(outputJson))
	outputFile.close
	

def heatmap(inputJson, title, xtitle, ytitle):

    #https://www.highcharts.com/demo/heatmap

    xcategories = []
    ycategories = []
    mydata = []

    init = True
    for x in inputJson:
        # print 'x',x
        if init is True:
            variablenames =[]
            for key,value in x.iteritems():
                variablenames.append(str(key))
                init = False
            # print 'variablenames:', str(variablenames)
        # print 'inputdata:', str(x[variablenames[0]]), str(x[variablenames[1]]), str(x[variablenames[2]])
        if str(x[variablenames[0]]) not in xcategories:
            xcategories.append(str(x[variablenames[0]]))
        if str(x[variablenames[1]]) not in ycategories:
            ycategories.append(str(x[variablenames[1]]))
        mydata.append([xcategories.index(str(x[variablenames[0]])),ycategories.index(str(x[variablenames[1]])),float(x[variablenames[2]])])

    # print 'xcategories',str(xcategories)
    # print 'ycategories',str(ycategories)
    # print 'mydata', str(mydata)

    myresult="chart: {  type: 'heatmap', marginTop: 40, marginBottom: 80, plotBorderWidth: 1 },"
    myresult += " title: { text: '" + title + "' },"
    myresult += " xAxis: { categories: " + str(xcategories) + ",title: { enabled: true,  style: { fontWeight: 'normal'}, text: '" + xtitle +"'}},"
    myresult += " yAxis: { categories: " + str(ycategories) + ",title: { enabled: true,  style: { fontWeight: 'normal'}, text: '" + ytitle +"'}},"
    myresult += " colorAxis: { min: 0, minColor: '#FFFFFF', maxColor: Highcharts.getOptions().colors[0] },"
    myresult += " legend: { align: 'right',layout: 'vertical', margin: 0, verticalAlign: 'top', y: 25, symbolHeight: 280 },"
    myresult += "  tooltip: {formatter: function () {return '<b> (' + this.series.xAxis.categories[this.point.x] + ',' + this.series.yAxis.categories[this.point.y] +')=' +this.point.value + '</b>'; } },"
    myresult += " series: [{  borderWidth: 1, data: "
    myresult += str(mydata)
    myresult += ", dataLabels: { enabled: true,color: '#000000'}}]"
    return myresult

if __name__ == "__main__":
    main()