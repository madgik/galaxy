#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys


def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
            argv = argv[2:]
        else:
            argv = argv[1:]
    return opts


def heatmap(
    inputJson,
    title,
    xtitle,
    ytitle,
    ):

    # https://www.highcharts.com/demo/heatmap

    xcategories = []
    ycategories = []
    mydata = []

    init = True
    for x in inputJson:

        # print 'x',x

        if init is True:
            variablenames = []
            for (key, value) in x.iteritems():
                variablenames.append(str(key))
                init = False

            # print 'variablenames:', str(variablenames)
        # print 'inputdata:', str(x[variablenames[0]]), str(x[variablenames[1]]), str(x[variablenames[2]])

        if str(x[variablenames[0]]) not in xcategories:
            xcategories.append(str(x[variablenames[0]]))
        if str(x[variablenames[1]]) not in ycategories:
            ycategories.append(str(x[variablenames[1]]))
        mydata.append([xcategories.index(str(x[variablenames[0]])),
                      ycategories.index(str(x[variablenames[1]])),
                      float(x[variablenames[2]])])

    consufion_matrix = {
        'chart': {
            'type': 'heatmap',
            'marginTop': 40,
            'marginBottom': 80,
            'plotBorderWidth': 1,
            },
        'title': {'text': 'Confusion Matrix'},
        'xAxis': {'categories': str(xcategories),
                  'title': {'enabled': True,
                  'style': {'fontWeight': 'normal'},
                  'text': str(xtitle)}},
        'yAxis': {'categories': str(ycategories),
                  'title': {'enabled': True,
                  'style': {'fontWeight': 'normal'},
                  'text': str(ytitle)}},
        'colorAxis': {'min': 0, 'minColor': '#FFFFFF',
                      'maxColor': '#6699ff'},
        'legend': {
            'align': 'right',
            'layout': 'vertical',
            'margin': 0,
            'verticalAlign': 'top',
            'y': 25,
            'symbolHeight': 280,
            },
        'tooltip': {'enabled': False},
        'series': [{'borderWidth': 1, 'data': mydata,
                   'dataLabels': {'enabled': True, 'color': '#000000'
                   }}],
        }

    return consufion_matrix


def main():
    args = sys.argv[1:]

    opts = getopts(args)

    if not opts or len(opts) < 5:
        print 'Usage:'
        print ' -in Input'
        print ' -t Title'
        print ' -xt xTitle'
        print ' -yt yTitle'
        print ' -o Output'
        return 0

    try:
        inputFile = open(opts.get('-in'), 'r')
        inputData = inputFile.read()
        inputJson = json.loads(inputData)
        title = opts.get('-t')
        xtitle = opts.get('-xt')
        ytitle = opts.get('-yt')
        previousResults = inputJson['results']
    except ValueError:
        print 'Input file should be:'
        print '{'
        print '  "results" : [ ... ]'
        print '}'

    results = []
    for previousResult in previousResults:
        result = {'result': [{'data': heatmap(previousResult, title,
                  xtitle, ytitle),
                  'type': 'application/vnd.highcharts+json'}]}
        results.append(result)

    outputFile = open(opts.get('-o'), 'w')
    outputFile.write(json.dumps(results))
    outputFile.close


if __name__ == '__main__':
    main()
