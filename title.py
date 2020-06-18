import json

if __name__ == '__main__':
    sections: list = json.load(open('_pawsSection.raw.json', 'r'))

    titles = set()
    for section in sections:
        titles.add(section['title'][0])

    titles = list(titles)
    titles.sort()

    json.dump(titles, open('title.json', 'w'), indent=4)
    json.dump(titles, open('title.min.json', 'w'), separators=(',', ':'))
