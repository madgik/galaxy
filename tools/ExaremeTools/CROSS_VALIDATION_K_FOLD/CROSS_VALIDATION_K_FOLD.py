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
		
	if not opts or len(opts) < 5:
		print("Usage:")
		print(" -d Datasets")
		print(" -col Columns")
		print(" -cl Classname")
		print(" -k KFold")
		print(" -o Output")
		return 0
		
	headers = {'Content-type': 'application/json', "Accept": "text/plain"}
	url= endpoint + '/mining/query/CROSS_VALIDATION_K_FOLD'
	data = [
		  {
			"name": "datasets",
			"value": opts.get("-d")
		  },
		  {
			"name": "columns",
			"value": opts.get("-col")
		  },
		  {
			"name": "classname",
			"value": opts.get("-cl")
		  },
		  {
			"name": "kfold",
			"value": opts.get("-k")
		  }
		]
	r = requests.post(url,data=json.dumps(data),headers=headers)
	outputFile = open(opts.get("-o"), "w")
	outputFile.write(r.text)
	outputFile.close
	
if __name__ == "__main__":
    main()