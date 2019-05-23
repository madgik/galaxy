import requests
import json
import sys

endpoint='http://88.197.53.36:9090'


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
		print(" -d Dataset")
		print(" -col Columns")
		print(" -cl Classname")
		print(" -tes Test Size (Optional)")
		print(" -trs Train Size (Optional)")
		print(" -rans Random State (Optional)")
		print(" -sh Shuffle (Optional)")
		print(" -o Output")
		return 0
		
	headers = {'Content-type': 'application/json', "Accept": "text/plain"}
	url= endpoint + '/mining/query/HOLD_OUT_VALIDATION'
	data = [
		  {
			"name": "dataset",
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
			"name": "test_size",
			"value": opts.get("-tes")
		  },
		  {
			"name": "train_size",
			"value": opts.get("-trs")
		  },
		  {
			"name": "random_state",
			"value": opts.get("-rans")
		  },
		  {
			"name": "shuffle",
			"value": opts.get("-sh")
		  }
		]
	print (json.dumps(data))
	response = requests.post(url,data=json.dumps(data),headers=headers)
	
	data = json.loads(response.text)
	data['numberOfSplits'] = '1'
		
	outputFile = open(opts.get("-o"), "w")
	outputFile.write(json.dumps(data))
	outputFile.close
	
if __name__ == "__main__":
    main()
