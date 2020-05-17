import json

if __name__ == '__main__':
    courses: list = json.load(open('_pawsCourse.raw.json', 'r'))

    courseAttributes = set()
    for course in courses:
        courseAttributes.update(course['courseAttributes'])

    courseAttributes = list(courseAttributes)
    courseAttributes.sort()

    json.dump(courseAttributes, open('courseAttribute.json', 'w'), indent=4)
    json.dump(courseAttributes, open('courseAttribute.min.json', 'w'), separators=(',', ':'))
