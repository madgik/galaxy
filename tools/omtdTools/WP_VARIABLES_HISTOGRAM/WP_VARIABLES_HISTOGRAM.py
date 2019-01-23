import requests
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
	
def main():
	args = sys.argv[1:]

	try:
		opts = getopts(args)
	except IndexError:
		print("Usage:")
		print(" -c1 Column1")
		print(" -c2 Column 2")
		print(" -nb NoOfBuckets")
		print(" -d Dataset")
		print(" -f Filter")
		print(" -o Output")
		return 0
		
	headers = {'Content-type': 'application/json', "Accept": "text/plain"}
	url='http://prozac.madgik.di.uoa.gr:9090/mining/query/WP_VARIABLES_HISTOGRAM'
	data = [
		  {
			"name": "column1",
			"value": opts.get("-c1")
		  },
		  {
			"name": "column2",
			"value": opts.get("-c2")
		  },
		  {
			"name": "nobuckets",
			"value": opts.get("-nb")
		  },
		  {
			"name": "dataset",
			"value": opts.get("-d")
		  },
		  {
			"name": "filter",
			"value": opts.get("-f")
		  }
		]
	r = requests.post(url,data=json.dumps(data),headers=headers)
	outputFile = open(opts.get("-o"), "w")
	outputFile.write(r.text)
	outputFile.close
	
if __name__ == "__main__":
    main()