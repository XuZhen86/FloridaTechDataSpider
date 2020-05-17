import json

if __name__ == '__main__':
    courses: list = json.load(open('_pawsCourse.raw.json', 'r'))

    scheduleTypes = set()
    for course in courses:
        scheduleTypes.update(course['scheduleTypes'])

    scheduleTypes = list(scheduleTypes)
    scheduleTypes.sort()

    json.dump(scheduleTypes, open('scheduleType.json', 'w'), indent=4)
    json.dump(scheduleTypes, open('scheduleType.min.json', 'w'), separators=(',', ':'))
