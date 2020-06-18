import json

if __name__ == '__main__':
    sections: list = json.load(open('_pawsSection.raw.json', 'r'))

    notes = set()
    for section in sections:
        for note in section['notes']:
            notes.add(note)

    notes = list(notes)
    notes.sort()

    json.dump(notes, open('note.json', 'w'), indent=4)
    json.dump(notes, open('note.min.json', 'w'), separators=(',', ':'))
