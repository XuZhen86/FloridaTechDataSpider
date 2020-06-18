import json

if __name__ == '__main__':
    sections: list = json.load(open('_pawsSection.raw.json', 'r'))

    sessions = set()
    for section in sections:
        session: str = section['session']
        if session is not None:
            sessions.add(session)

    sessions = list(sessions)
    sessions.sort()

    json.dump(sessions, open('session.json', 'w'), indent=4)
    json.dump(sessions, open('session.min.json', 'w'), separators=(',', ':'))
