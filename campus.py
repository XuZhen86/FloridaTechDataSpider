import json

if __name__ == '__main__':
    sections: list = json.load(open('_section.raw.json', 'r'))

    campuses = set()
    for section in sections:
        campuses.add(section['location'])

    campuses = list(campuses)
    campuses.sort()

    json.dump(campuses, open('campus.json', 'w'), indent=4)
    json.dump(campuses, open('campus.min.json', 'w'), separators=(',', ':'))
