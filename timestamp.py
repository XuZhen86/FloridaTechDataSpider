import json
from datetime import datetime

json.dump(datetime.now().timestamp(), open('timestamp.json', 'w'))
