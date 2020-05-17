import json
import re

import scrapy


def parseLevels(text: str, texts: list, section: dict) -> None:
    if text.strip() == 'Levels:':
        section['level'] = texts.pop().strip()


def parseWaitListSeats(text: str, texts: list, section: dict) -> None:
    if text.strip() != 'Registration Availability':
        return

    while texts[-1].strip() != 'Waitlist Seats':
        texts.pop()

    seats = []
    texts.pop()
    texts.pop()

    seats.append(int(texts.pop()))
    texts.pop()

    seats.append(int(texts.pop()))
    texts.pop()

    section['waitListSeats'] = seats


def parseCrossListCoruses(text: str, texts: list, section: dict) -> None:
    if text.strip() != 'Cross List Courses:':
        return

    courses = []
    texts.pop()
    texts.pop()

    while texts[-1].strip() != '':
        text: str = texts.pop()

        course = text.split(' ')
        course[1] = int(course[1])

        courses.append(course)
        texts.pop()
        texts.pop()

    section['crossListCourses'] = courses


def parseRestrictions(text: str, texts: list, section: dict) -> None:
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

    section['restrictions'] = restrictions


def parsePrerequisites(text: str, texts: list, section: dict) -> None:
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

    section['prerequisite'] = prerequisite



class PawsSectionSpider(scrapy.Spider):
    name = 'pawsSection'
    allowed_domains = ['nssb-p.adm.fit.edu']

    sectionAttributes = [
        {
            'key': 'level',
            'parseFn': parseLevels,
            'default': None
        }, {
            'key': 'waitListSeats',
            'parseFn': parseWaitListSeats,
            'default': []
        }, {
            'key': 'crossListCourses',
            'parseFn': parseCrossListCoruses,
            'default': []
        }, {
            'key': 'restrictions',
            'parseFn': parseRestrictions,
            'default': []
        }, {
            'key': 'prerequisite',
            'parseFn': parsePrerequisites,
            'default': None
        }
    ]

    def start_requests(self):
        # yield scrapy.Request(
        #     'https://nssb-p.adm.fit.edu/prod/bwckschd.p_disp_detail_sched?term_in=202001&crn_in=19836',
        #     callback=self.parsePawsSection,
        #     cb_kwargs={
        #         'section': dict()
        #     }
        # )

        # yield scrapy.Request(
        #     'https://nssb-p.adm.fit.edu/prod/bwckschd.p_disp_detail_sched?term_in=202001&crn_in=25783',
        #     callback=self.parsePawsSection,
        #     cb_kwargs={
        #         'section': dict()
        #     }
        # )

        term = ['', 'spring', '', '', '', 'summer', '', '', 'fall']

        sections: list = json.load(open('_section.raw.json', 'r'))
        # for section in sections[0:100]:
        for section in sections:
            year: int = section['year']
            semester: str = section['semester']
            crn: int = section['crn']

            termIn: str = f'{year}{"{:02}".format(term.index(semester))}'
            pawsUrl = f'https://nssb-p.adm.fit.edu/prod/bwckschd.p_disp_detail_sched?term_in={termIn}&crn_in={crn}'
            # print(pawsUrl)

            yield scrapy.Request(
                pawsUrl,
                callback=self.parsePawsSection,
                cb_kwargs={
                    'section': section
                }
            )

    def parsePawsSection(self, response: scrapy.http.Response, section: dict) -> None:
        # print(response.url)

        texts: list = response.xpath('''
            //table[@class="datadisplaytable" and @summary="This table is used to present the detailed class information."]
            //td[@class="dddefault"]
            //text()
        ''').getall()

        # for text in texts:
        #     print(f'[{text}]')

        texts.reverse()

        section.update({
            attribute['key']: attribute['default']
            for attribute in self.sectionAttributes
        })

        while texts != []:
            text: str = texts.pop()
            if text.strip() == '':
                continue

            for attribute in self.sectionAttributes:
                key: str = attribute['key']
                parseFn = attribute['parseFn']
                default = attribute['default']

                if section[key] == default:
                    parseFn(text, texts, section)

        # print(section)
        yield section
