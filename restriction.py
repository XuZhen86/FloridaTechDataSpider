import json

if __name__ == '__main__':
    courses: list = json.load(open('_pawsCourse.raw.json', 'r'))
    sections: list = json.load(open('_pawsSection.raw.json', 'r'))

    restrictions = set()
    for course in courses:
        restrictions.update(course['restrictions'])
    for section in sections:
        restrictions.update(section['restrictions'])

    restrictions = list(restrictions)
    restrictions.sort()

    json.dump(restrictions, open('restriction.json', 'w'), indent=4)
    json.dump(restrictions, open('restriction.min.json', 'w'), separators=(',', ':'))
