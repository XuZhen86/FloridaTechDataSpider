import bisect
import json
from dataclasses import asdict, astuple, dataclass, field, fields


@dataclass
class Course:
    subjectId: int
    course: int

    campusId: int
    semesterId: int
    year: int

    creditHours: list = None
    sectionIds: list = None
    titleId: int = None
    descriptionId: int = None
    tagIds: set = None

    lectureHours: int = None
    labHours: int = None

    levelId: int = None
    scheduleTypeIds: list = None
    restrictionIds: list = None
    prerequisiteId: int = None
    courseAttributeIds: list = None


# https://docs.python.org/3/library/bisect.html#searching-sorted-lists
def bisectIndex(ls: list, value) -> int:
    if value is None:
        return -1

    index = bisect.bisect_left(ls, value)
    if index != len(ls) and ls[index] == value:
        return index

    return -1


if __name__ == '__main__':
    subjects: list = json.load(open('subject.json', 'r'))
    subjects = [
        subject['code']
        for subject in subjects
    ]

    courses: list = json.load(open('course2.json', 'r'))

    for course in courses:
        subjectCode: str = course['subject']
        subjectId = bisectIndex(subjects, subjectCode)
        course['subjectId'] = subjectId

    keys = [f.name for f in fields(Course)]
    courses = [
        Course(**{key: c[key] for key in keys})
        for c in courses
    ]
    values = [list(astuple(c)) for c in courses]

    json.dump(
        [asdict(c) for c in courses],
        open('course3.json', 'w'),
        indent=4
    )
    json.dump(
        {'keys': keys, 'values': values},
        open('course3.min.json', 'w'),
        separators=(',', ':')
    )
