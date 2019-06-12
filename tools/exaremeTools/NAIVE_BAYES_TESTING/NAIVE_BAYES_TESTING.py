import requests
import json
import sys

execfile('/srv/executor/tools/exaremeTools/exareme_environment.py')

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
		
	if not opts or len(opts) < 4:
		print("Usage:")
		print(" -in Input")
		print(" -x X")
		print(" -y Y")
		print(" -o Output")
		return 0

	try:
		inputFile = open(opts.get("-in"), "r")
		inputData = inputFile.read()
		inputJson = json.loads(inputData)
		dbIdentifier = inputJson['dbIdentifier']
		models = inputJson['models']
	except ValueError:  # includes simplejson.decoder.JSONDecodeError
		print("Input file should be:")
		print("{")
		print('  "models" : [ ... ],')
		print('  "dbIdentifier" : "randomIdentifier"')
		print("}")
		
	responses = []
	for i in xrange(len(models)):
		headers = {'Content-type': 'application/json', "Accept": "text/plain"}
		url= endpoint + '/mining/query/NAIVE_BAYES_TESTING'
		data = [
			  {
				"name": "iterationNumber",
				"value": str(i)
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
				"value": json.dumps(models[i])
			  }
			]
		response = json.loads(requests.post(url,data=json.dumps(data),headers=headers).text)
		if "error" in response:
			raise ValueError(json.dumps(response))
		responses.append(response)
	
	data = {"results" : responses}
	
	outputFile = open(opts.get("-o"), "w")
	outputFile.write(json.dumps(data))
	outputFile.close
	
if __name__ == "__main__":
    main()
