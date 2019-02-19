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
		dbIdentifier = inputJson['dbIdentifier']
		numberOfSplits = inputJson['numberOfSplits']
		models = inputJson['models']
	except ValueError:  # includes simplejson.decoder.JSONDecodeError
		print("Input file should be:")
		print("{")
		print('  "dbIdentifier" : "randomIdentifier"')
		print('  "numberOfSplits" : "5"')
		print("}")
		
	responses = []
	for i in xrange(int(numberOfSplits)):
		headers = {'Content-type': 'application/json', "Accept": "text/plain"}
		url= endpoint + '/mining/query/NAIVE_BAYES_TESTING'
		data = [
			  {
				"name": "iterationNumber",
				"value": str(i)
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
		responses.append(response)
	
	data = {"numberOfSplits" : numberOfSplits}
	data['results'] = responses
	
	outputFile = open(opts.get("-o"), "w")
	outputFile.write(json.dumps(data))
	outputFile.close
	
if __name__ == "__main__":
    main()