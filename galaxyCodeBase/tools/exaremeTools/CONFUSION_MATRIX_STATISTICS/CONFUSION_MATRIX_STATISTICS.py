import json
import sys
from rpy2.robjects import StrVector
from rpy2.robjects.packages import importr
from rpy2.rinterface import RRuntimeError

import warnings
warnings.filterwarnings("ignore")

try:
    caret = importr('caret')
except RRuntimeError:
    utils = importr('utils')
    utils.install_packages('caret')
    caret = importr('caret')


try:
    e = importr('e1071')
except RRuntimeError:
    utils = importr('utils')
    utils.install_packages('e1071')
    e = importr('e1071')

base = importr('base')


def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
            argv = argv[2:]
        else:
            argv = argv[1:]
    return opts


def Rfunction_confusionmatrix(inputjson):
    #data:  a factor of predicted classes
    #reference: a factor of classes to be used as the true results

    data = []
    reference = []
    classnames = []
    resultdict = {}

    init = True
    for x in inputjson:
        # print 'x',x
        if init is True:
            variablenames =[]
            for key,value in x.iteritems():
                variablenames.append(str(key))
                init = False
            # print 'variablenames:', str(variablenames)
        # print 'inputdata:', str(x[variablenames[0]]), str(x[variablenames[1]]), str(x[variablenames[2]])
        for v in xrange(int(x[variablenames[2]])):
            reference.append(str(x[variablenames[0]]))
            data.append(str(x[variablenames[1]]))
            if str(x[variablenames[0]]) not in  classnames:
                classnames.append(str(x[variablenames[0]]))

    # print "Predicted vector:", str(data)
    # print "Actual vector:", str(reference)

    numberofclassnames = len(classnames)

    # print 'numberofclassnames', str(numberofclassnames)
    # print 'variablenames', str(variablenames)
    # print str(reference)
    # print str(data)
    # print 'classnames', str(classnames)

    Rresult = caret.confusionMatrix(base.factor(StrVector(data)),base.factor(StrVector(reference)))

    jsonResult = '{"overall": {'


    if numberofclassnames == 2:
        jsonResult += '"Positive Class":"' + Rresult[0][0]+'",'
    else:
        jsonResult += '"Positive Class":"' + '' +'",'

    #Rresult[1] -->Table (I have already computed this)

    #Rresult[2] -->overall statistics
    jsonResult += '"Accuracy":' + str(Rresult[2][0]) +','
    jsonResult += '"Kappa":' + str(Rresult[2][1]) +','
    jsonResult += '"AccuracyLower":' + str(Rresult[2][2]) +','
    jsonResult += '"AccuracyUpper":' + str(Rresult[2][3]) +','
    jsonResult += '"AccuracyNull":' + str(Rresult[2][4]) +','
    jsonResult += '"AccuracyPValue":' + str(Rresult[2][5]) +','
    jsonResult += '"McnemarPValue":' + str(Rresult[2][6]) +'},'

    #Rresult[3] -->byClass statistics
    for i in xrange(len(classnames)-1):
        # print i,classnames[i]
        j = i*10

        jsonResult += '"Class name: '+ classnames[i] +'":{'
        jsonResult += '"Sensitivity":' + str(Rresult[3][j+0]) + ','
        jsonResult += '"Specificity":' + str(Rresult[3][j+1]) + ','
        jsonResult += '"Pos Pred Value":' + str(Rresult[3][j+2]) + ','
        jsonResult += '"Neg Pred Value":' + str(Rresult[3][j+3]) + ','
        jsonResult += '"Precision":' + str(Rresult[3][j+4]) + ','
        jsonResult += '"Recall":' + str(Rresult[3][j+5]) + ','
        jsonResult += '"F1":' + str(Rresult[3][j+6]) + ','
        jsonResult += '"Prevalence":' + str(Rresult[3][j+7]) + ','
        jsonResult += '"Detection Rate":' + str(Rresult[3][j+8]) + ','
        jsonResult += '"Detection Prevalence":' + str(Rresult[3][j+9]) + ','
        jsonResult += '"Balanced Accuracy":'+ str(Rresult[3][j+10]) +'}'
        if i == len(classnames)-2:
            jsonResult += '}'
        else:
            jsonResult += ','

        jsonResult = jsonResult.replace(":nan",":null")
        jsonResult = jsonResult.replace(":NA",":null")

    return jsonResult

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
    except ValueError:
        print("Input file should be:")
        print('[{ "result" : [{')
        print('  "data": [...],')
        print('  "type": "application/json"')
        print('   } , ... ')
        print('] }')
    
    statistics = []
    for i in xrange(len(inputJson)):
        try:
            result = {'result': [{'data': Rfunction_confusionmatrix(inputJson[i]['result'][0]['data']),'type': 'text'}]}
        except ValueError:
            print("Input file should be:")
            print('[{ "result" : [{')
            print('  "data": [...],')
            print('  "type": "application/json"')
            print('   } , ... ')
            print('] }')
        statistics.append(result)
    
    outputFile = open(opts.get("-o"), "w")
    outputFile.write(json.dumps(statistics))
    outputFile.close

if __name__ == "__main__":
    main()