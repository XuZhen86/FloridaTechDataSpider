import json
import sys

data = json.load(open(sys.argv[1], 'r'))
json.dump(data, open(sys.argv[1], 'w'), indent=4)
