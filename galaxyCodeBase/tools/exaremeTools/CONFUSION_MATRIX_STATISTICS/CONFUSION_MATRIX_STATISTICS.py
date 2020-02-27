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

    print "Predicted vector:", str(data)
    print "Actual vector:", str(reference)

    numberofclassnames = len(classnames)

    # print 'numberofclassnames', str(numberofclassnames)
    # print 'variablenames', str(variablenames)
    # print str(reference)
    # print str(data)
    # print 'classnames', str(classnames)

    Rresult = caret.confusionMatrix(base.factor(StrVector(data)),base.factor(StrVector(reference)))

    #####################################################
    dataOverall = []
    if numberofclassnames == 2:
        dataOverall.append(["Positive Class",Rresult[0][0]])
    else:
        dataOverall.append(["Positive Class",None])

    #Rresult[1] -->Table (I have already computed this)

    #Rresult[2] -->overall statistics
    dataOverall.append(["Accuracy",(Rresult[2][0])])
    dataOverall.append(["Kappa",(Rresult[2][1])])
    dataOverall.append(["AccuracyLower",(Rresult[2][2])])
    dataOverall.append(["AccuracyUpper",(Rresult[2][3])])
    dataOverall.append(["AccuracyNull",(Rresult[2][4])])
    dataOverall.append(["AccuracyPValue",(Rresult[2][5])])
    dataOverall.append(["McnemarPValue",(Rresult[2][6])])

    ResultOverall = { "data": {
            "profile": "tabular-data-resource",
            "data": dataOverall,
            "name": "Overall",
            "schema": {
              "fields": [
                {
                  "type": "text",
                  "name": "StatisticName"
                },
                {
                  "type": "real",
                  "name": "Value"
                }
              ]
            }
          },
          "type": "application/vnd.dataresource+json"
        }
    #####################################################

    FieldClassNames =  [
      { "type": "text",
        "name": "StatisticName" }]
    for i in xrange(len(classnames)-1):
        FieldClassNames.append(
          {
            "type": "real",
            "name": classnames[i] +"' class"
          })

    DataClassNames = [["Sensitivity"],["Specificity"],["Pos Pred Value"],["Neg Pred Value"],["Precision"],["Recall"],
    ["F1"],["Prevalence"],["Detection Rate"],["Detection Prevalence"],["Balanced Accuracy"]]

    #Rresult[3] -->byClass statistics
    for i in xrange(len(classnames)-1):
        # print i,classnames[i]
        j = i*10
        for k in xrange(11):
            if str(Rresult[3][j+k])!='nan' and str(Rresult[3][j+k])!='NA':
                DataClassNames[k].append((Rresult[3][j+k]))
            else:
                DataClassNames[k].append(None)


    ResultClassNames = {
    "data": {
            "profile": "tabular-data-resource",
            "data": DataClassNames,
            "name": "ClassNames",
            "schema": { "fields": FieldClassNames}
            },
   "type": "application/vnd.dataresource+json"}


    jsonResult = [ ResultOverall, ResultClassNames ]
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
            result = Rfunction_confusionmatrix(inputJson[i]['result'][0]['data'])
        except ValueError:
            print("Input file should be:")
            print('[{ "result" : [{')
            print('  "data": [...],')
            print('  "type": "application/json"')
            print('   } , ... ')
            print('] }')
        statistics.append(result[0])
        statistics.append(result[1])
    
    finalResult={ "result" : statistics }
    
    outputFile = open(opts.get("-o"), "w")
    outputFile.write(json.dumps(finalResult))
    outputFile.close

if __name__ == "__main__":
    main()