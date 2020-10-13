import requests
import json
import sys

execfile('/galaxy/tools/exaremeTools/exareme_environment.py')

endpoint = 'http://' + EXAREME_IP + ':' + EXAREME_PORT


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
        
    if not opts or len(opts) < 6:
        print("Usage:")
        print(" -in Input")
        print(" -p Pathology")
        print(" -d Dataset")
        print(" -x X")
        print(" -y Y")
        print(" -o Output")
        return 0
    try:
        inputFile = open(opts.get("-in"), "r")
        inputData = inputFile.read()
        inputJson = json.loads(inputData)
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print("Input file should be:")
        print('[{ "result" : [{')
        print('  "data": [...],')
        print('  "type": "application/json",')
        print('  "dbIdentifier": "CROSS_VALIDATION_K_FOLD_1574239799896"')
        print('   } , ... ')
        print('] }')

    responses = []
    for i in xrange(len(inputJson)):
        try:
            dbIdentifier = inputJson[i]['result'][0]['dbIdentifier']
            model = inputJson[i]['result'][0]['data']
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print("Input file should be:")
            print('[{ "result" : [{')
            print('  "data": [...],')
            print('  "type": "application/json",')
            print('  "dbIdentifier": "CROSS_VALIDATION_K_FOLD_1574239799896"')
            print('   } , ... ')
            print('] }')
    
        headers = {'Content-type': 'application/json', "Accept": "text/plain"}
        url= endpoint + '/mining/query/NAIVE_BAYES_TESTING'
        data = [
              {
                "name": "iterationNumber",
                "value": str(i)
              },
              {
                "name": "pathology",
                "value": opts.get("-p")
              },
              {
                "name": "dataset",
                "value": opts.get("-d")
              },
              {
                "name": "x",
                "value": opts.get("-x")
              },
              {
                "name": "y",
                "value": opts.get("-y")
              },
              {
                "name": "dbIdentifier",
                "value": dbIdentifier
              },
              {
                "name": "model",
                "value": json.dumps(model)
              }
            ]
        response = json.loads(requests.post(url,data=json.dumps(data),headers=headers).text)
        if 'result' in response:
            if 'error' in response['result'][0]['type'] or 'warning' in response['result'][0]['type']:
                raise ValueError(json.dumps(response))
        responses.append(response)
        
    outputFile = open(opts.get("-o"), "w")
    outputFile.write(json.dumps(responses))
    outputFile.close
    
if __name__ == "__main__":
    main()
