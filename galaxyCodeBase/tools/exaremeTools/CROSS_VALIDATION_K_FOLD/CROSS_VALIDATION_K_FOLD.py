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
        print(" -p Pathology")
        print(" -d Dataset")
        print(" -x X")
        print(" -y Y")
        print(" -f (Optional) Filter")
        print(" -k KFold")
        print(" -o Output")
        return 0
        
    headers = {'Content-type': 'application/json', "Accept": "text/plain"}
    url= endpoint + '/mining/query/CROSS_VALIDATION_K_FOLD'
    data = [
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
            "name": "filter",
            "value": opts.get("-f")
          },
          {
            "name": "kfold",
            "value": opts.get("-k")
          }
        ]
    response = requests.post(url,data=json.dumps(data),headers=headers)
    
    data = json.loads(response.text)
    if 'result' in data:
        if 'error' in data['result'][0]['type'] or 'warning' in data['result'][0]['type']:
            raise ValueError(json.dumps(data))
    
    data['result'][0]['numberOfSplits'] = opts.get("-k")
    
    outputFile = open(opts.get("-o"), "w")
    outputFile.write(json.dumps(data))
    outputFile.close
    
if __name__ == "__main__":
    main()
