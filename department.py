import json
import re
import bisect
from dataclasses import asdict, astuple, dataclass, fields


@dataclass
class Department:
    code: str
    name: str
    phone: str
    fax: str
    email: str
    website: str
    buildingId: int

    def __lt__(self, d) -> bool:
        return self.code < d.code

# https://docs.python.org/3/library/bisect.html#searching-sorted-lists
def bisectIndex(ls: list, value):
    if value is None:
        return -1

    index = bisect.bisect_left(ls, value)
    if index != len(ls) and ls[index] == value:
        return index

    return -1


if __name__ == '__main__':
    departments = json.load(open('_department.raw.json', 'r'))
    buildings = json.load(open('building.json', 'r'))

    buildings = [b["code"] for b in buildings]

    for department in departments:
        buildingText: str = department['primaryLocation']

        try:
            duplets = re.match(r'(.+) \((\d{3}\w{3})\)', buildingText).groups()
            locationCode = duplets[1]
        except TypeError:
            locationCode = None

        department['buildingId'] = bisectIndex(buildings, locationCode)

    keys = [f.name for f in fields(Department)]
    departments = [
        Department(**{key: d[key] for key in keys})
        for d in departments
    ]
    departments.sort()
    values = [list(astuple(d)) for d in departments]

    json.dump(
        [asdict(d) for d in departments],
        open('department.json', 'w'),
        indent=4
    )
    json.dump(
        {'keys': keys, 'values': values},
        open('department.min.json', 'w'),
        separators=(',', ':')
    )
