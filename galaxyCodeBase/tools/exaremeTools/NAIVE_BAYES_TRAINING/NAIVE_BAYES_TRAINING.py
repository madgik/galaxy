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
		
	if not opts or len(opts) < 7:
		print("Usage:")
		print(" -in Input")
		print(" -p Pathology")
		print(" -d Dataset")
		print(" -x X")
		print(" -y Y")
		print(" -a Alpha")
		print(" -o Output")
		return 0

	try:
		inputFile = open(opts.get("-in"), "r")
		inputData = inputFile.read()
		inputJson = json.loads(inputData)
		dbIdentifier = inputJson['dbIdentifier']
		numberOfSplits = inputJson['numberOfSplits']
	except ValueError:  # includes simplejson.decoder.JSONDecodeError
		print("Input file should be:")
		print("{")
		print('  "dbIdentifier" : "randomIdentifier",')
		print('  "numberOfSplits" : "5"')
		print("}")
		
	responses = []
	for i in xrange(int(numberOfSplits)):
		headers = {'Content-type': 'application/json', "Accept": "text/plain"}
		url= endpoint + '/mining/query/NAIVE_BAYES_TRAINING'
		data = [
			  {
				"name": "alpha",
				"value": opts.get("-a")
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
				"name": "iterationNumber",
				"value": str(i)
			  },
			  {
				"name": "dbIdentifier",
				"value": dbIdentifier
			  }
			]
		response = json.loads(requests.post(url,data=json.dumps(data),headers=headers).text)
		if "error" in response:
			outputFile = open(opts.get("-o"), "w")
			outputFile.write(json.dumps(response))
			outputFile.close
			raise ValueError(json.dumps(response))
		responses.append(response['results'])
	
	data = {'dbIdentifier' : dbIdentifier}
	data['models'] = responses
	
	outputFile = open(opts.get("-o"), "w")
	outputFile.write(json.dumps(data))
	outputFile.close
	
if __name__ == "__main__":
    main()
