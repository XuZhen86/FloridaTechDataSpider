import json
import re

import scrapy


lectureHoursPattern = re.compile(
    pattern=r'([\d.]+)\s+Lecture hours',
    flags=re.IGNORECASE
)


def parseLectureHours(text: str, texts: list, course: dict) -> None:
    text = text.strip()
    try:
        course['lectureHours'] = float(
            lectureHoursPattern.search(text).group(1))
    except AttributeError:  # 'NoneType' object has no attribute 'group'
        pass


labHoursPattern = re.compile(
    pattern=r'([\d.]+)\s+Lab hours',
    flags=re.IGNORECASE
)


def parseLabHours(text: str, texts: list, course: dict) -> None:
    text = text.strip()
    try:
        course['labHours'] = float(labHoursPattern.search(text).group(1))
    except AttributeError:  # 'NoneType' object has no attribute 'group'
        pass


def parseLevels(text: str, texts: list, course: dict) -> None:
    if text.strip() == 'Levels:':
        course['level'] = texts.pop().strip()


def parseScheduleTypes(text: str, texts: list, course: dict) -> None:
    if text.strip() != 'Schedule Types:':
        return
        # course['scheduleType'] = texts.pop().strip()

    scheduleTypes = []

    text: str = texts.pop()
    while text.strip() != '':
        parts = text.strip().split(',')
        for part in parts:
            part = part.strip()
            if part != '':
                scheduleTypes.append(part)

        text: str = texts.pop()

    course['scheduleTypes'] = scheduleTypes


def parseRestrictions(text: str, texts: list, course: dict) -> None:
    if text.strip() != 'Restrictions:':
        return

    restrictions = []
    texts.pop()  # '\n'

    text: str = texts.pop()
    while text.strip() != '':
        if text.startswith('\n\xa0 \xa0 \xa0 '):
            restrictions.append('\t' + text.strip())
        else:
            restrictions.append(text.strip())

        text: str = texts.pop()

    course['restrictions'] = restrictions


def parsePrerequisites(text: str, texts: list, course: dict) -> None:
    if text.strip() != 'Prerequisites:':
        return

    prerequisite = ''
    texts.pop()  # '\n'

    text: str = texts.pop()
    while text.strip() != '':
        prerequisite += f'{text.strip()} '
        text: str = texts.pop()

    prerequisite = prerequisite.strip() # Remove trailing space
    if prerequisite == '':
        prerequisite = None

    course['prerequisite'] = prerequisite


def parseCourseAttributes(text: str, texts: list, course: dict) -> None:
    if text.strip() != 'Course Attributes:':
        return

    courseAttributes = []

    text: str = texts.pop()
    while text.strip() != '':
        courseAttributes.append(text.strip())
        text: str = texts.pop()

    course['courseAttributes'] = courseAttributes


class PawsCourseSpider(scrapy.Spider):
    name = 'pawsCourse'
    allowed_domains = ['nssb-p.adm.fit.edu']

    courseAttributes = [
        {
            'key': 'lectureHours',
            'parseFn': parseLectureHours,
            'default': None
        }, {
            'key': 'labHours',
            'parseFn': parseLabHours,
            'default': None
        }, {
            'key': 'level',
            'parseFn': parseLevels,
            'default': None
        }, {
            'key': 'scheduleTypes',
            'parseFn': parseScheduleTypes,
            'default': []
        }, {
            'key': 'restrictions',
            'parseFn': parseRestrictions,
            'default': []
        }, {
            'key': 'prerequisite',
            'parseFn': parsePrerequisites,
            'default': None
        }, {
            'key': 'courseAttributes',
            'parseFn': parseCourseAttributes,
            'default': []
        }
    ]

    def start_requests(self):
        courses: list = json.load(open('course.json', 'r'))
        for course in courses:
            subject: str = course['subject']
            courseNumber: int = course['course']
            semesterId: int = course['semesterId']
            year: int = course['year']

            catTermIn = f'{year}{["01", "05", "08"][semesterId]}'
            pawsUrl = f'https://nssb-p.adm.fit.edu/prod/bwckctlg.p_disp_course_detail?cat_term_in={catTermIn}&subj_code_in={subject}&crse_numb_in={courseNumber}'
            # print(pawsUrl)

            yield scrapy.Request(
                pawsUrl,
                callback=self.parsePawsCourse,
                cb_kwargs={
                    'course': course
                },
                dont_filter=True
            )

    def parsePawsCourse(self, response: scrapy.http.TextResponse, course: dict) -> None:
        # print(response.url)

        texts: list = response.xpath('''
            //table[@class="datadisplaytable" and @summary="This table lists the course detail for the selected term."]
            //td[@class="ntdefault"]
            //text()
        ''').getall()

        # print(texts)
        texts.reverse()

        course.update({
            attribute['key']: attribute['default']
            for attribute in self.courseAttributes
        })

        while texts != []:
            text: str = texts.pop()
            if text.strip() == '':
                continue

            for attribute in self.courseAttributes:
                key: str = attribute['key']
                parseFn = attribute['parseFn']
                default = attribute['default']

                if course[key] == default:
                    parseFn(text, texts, course)

        # print(course)
        yield course
