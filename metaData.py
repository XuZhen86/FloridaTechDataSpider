import json
import os
from datetime import datetime


fileNames = [
    'building.min.json',
    'campus.min.json',
    'course3.min.json',
    'courseAttribute.min.json',
    'department.min.json',
    'description.min.json',
    'employee.min.json',
    'level.min.json',
    'note.min.json',
    'prerequisite.min.json',
    'requirement.min.json',
    'restriction.min.json',
    'scheduleType.min.json',
    'section.min.json',
    'session.min.json',
    'subject.min.json',
    'tag.min.json',
    'title.min.json'
]


if __name__ == '__main__':
    fileSizes = {}
    for fileName in fileNames:
        size = os.path.getsize(fileName)
        fileSizes[fileName] = size

    timestamp = datetime.now().timestamp()

    json.dump(
        {'fileSizes': fileSizes, 'timestamp': timestamp},
        open('metaData.json', 'w'),
        indent=4
    )
    json.dump(
        {'fileSizes': fileSizes, 'timestamp': timestamp},
        open('metaData.min.json', 'w'),
        separators=(',', ':')
    )
