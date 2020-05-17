import re

import scrapy


def parseCourse(tableData: scrapy.Selector) -> list:
    text: str = tableData.xpath('text()').get()
    doublet = re.match(r'(\w{3,4}) (\d+)', text).groups()
    return [doublet[0], int(doublet[1])]


def parseCreditHours(tableData: scrapy.Selector) -> list:
    try:
        text: str = tableData.xpath('text()').get()
        doublet = re.match(r'([\d.]+)-([\d.]+)', text).groups()
        return [float(doublet[0]), float(doublet[1])]
    except AttributeError:
        return [float(text), float(text)]


def parseTitle(tableData: scrapy.Selector) -> list:
    return [
        tableData.xpath('span/text()').get().strip(),
        tableData.xpath('span/@data-content').get()
    ]


def parseNotes(tableData: scrapy.Selector) -> list:
    return [
        note.strip()
        for note in tableData.xpath('text()').getall()
        if note.strip() != ''
    ]


def parseDays(tableData: scrapy.Selector) -> list:
    return [
        day.strip()
        for day in tableData.xpath('text()').getall()
        if day.strip() != ''
    ]


def parseTimes(tableData: scrapy.Selector) -> list:
    return [
        [
            int(time)
            for time in timeRange.strip().split('-')
        ]
        for timeRange in tableData.xpath('text()').getall()
        if timeRange.strip() != ''
    ]


def parsePlaces(tableData: scrapy.Selector) -> list:
    places = []

    for placePair in tableData.xpath('text()').getall():
        placePair = placePair.strip()
        if placePair != '':
            places.append(placePair.split(' '))

    return places


def parseInstructor(tableData: scrapy.Selector) -> list:
    try:
        email = tableData.xpath('a/@href').get()
        email = email[len('mailto:'):]
        name = tableData.xpath('a/text()').get()
        return [name, email]
    except TypeError:
        return ['', '']


def parseCap(tableData: scrapy.Selector) -> list:
    return [
        int(tableData.xpath('strong/text()').get()),
        int(tableData.xpath('text()').get()[1:])
    ]


class SectionSpider(scrapy.Spider):
    name = 'section'
    allowed_domains = ['apps.fit.edu']
    start_urls = ['https://apps.fit.edu/schedule']

    sectionAttributes = [
        {
            'header': 'CRN',
            'key': 'crn',
            'default': None,
            'xpath': 'text()',
            'parseFn': None
        }, {
            'header': 'Course',
            'key': 'course',
            'default': ['', 0],
            'xpath': None,
            'parseFn': parseCourse
        }, {
            'header': 'Section',
            'key': 'section',
            'default': None,
            'xpath': 'text()',
            'parseFn': None
        }, {
            'header': 'Cr',
            'key': 'creditHours',
            'default': None,
            'xpath': None,
            'parseFn': parseCreditHours
        }, {
            'header': 'Title',
            'key': 'title',
            'default': None,
            'xpath': None,
            'parseFn': parseTitle
        }, {
            'header': 'Notes',
            'key': 'notes',
            'default': [],
            'xpath': None,
            'parseFn': parseNotes
        }, {
            'header': 'Session',
            'key': 'session',
            'default': None,
            'xpath': 'text()',
            'parseFn': None
        }, {
            'header': 'Days',
            'key': 'days',
            'default': [],
            'xpath': None,
            'parseFn': parseDays
        }, {
            'header': 'Times',
            'key': 'times',
            'default': [],
            'xpath': None,
            'parseFn': parseTimes
        }, {
            'header': 'Place',
            'key': 'places',
            'default': [],
            'xpath': None,
            'parseFn': parsePlaces
        }, {
            'header': 'Instructor',
            'key': 'instructor',
            'default': None,
            'xpath': None,
            'parseFn': parseInstructor
        }, {
            'header': 'Cap',
            'key': 'cap',
            'default': None,
            'xpath': None,
            'parseFn': parseCap
        }, {
            'header': 'Syllabus',
            'key': 'syllabus',
            'default': None,
            'xpath': 'a/@href',
            'parseFn': None
        }
    ]

    def parse(self, response: scrapy.http.TextResponse) -> None:
        # campusUrls will contain 'https://policy.fit.edu/Schedule-of-Classes'
        # This URL is automatically eliminated by self.allowed_domains
        campusUrls = response.xpath('''
            //div[@class="three wide column"]
            /div[@id="sub-nav"]
            /a
            /@href
        ''').getall()
        # print(campusUrls)

        yield from response.follow_all(campusUrls, callback=self.parseCampus)

    def parseCampus(self, response: scrapy.http.TextResponse) -> None:
        semesterUrls = response.xpath('''
            //div[@class="thirteen wide column"]
            /div[@class="ui"]
            /a
            /@href
        ''').getall()
        # print(semesterUrls)

        yield from response.follow_all(semesterUrls, callback=self.parseSemester)

    def parseSemester(self, response: scrapy.http.TextResponse) -> None:
        sectionTableUrls = [
            f'{response.url}?page=1'
        ]
        # print(sectionTableUrls)

        yield from response.follow_all(sectionTableUrls, callback=self.parseSectionTable)

    def parseSectionTable(self, response: scrapy.http.TextResponse) -> None:
        nextPageUrls = response.xpath('''
            //div[@class="thirteen wide column"]
            /div[@class="ui pagination menu"]
            /a
            /@href
        ''').getall()
        # print(nextPageUrls)

        yield from response.follow_all(nextPageUrls, callback=self.parseSectionTable)

        h2Text: str = response.xpath('''
            //div[@class="thirteen wide column"]
            /h2
            /text()
        ''').get()

        try:
            triplet = re.match(
                r'(.+) Class Schedule: (spring|summer|fall) (\d{4})',
                h2Text
            ).groups()
        except AttributeError:
            return

        location: str = triplet[0]
        semester: str = triplet[1]
        year = int(triplet[2])
        # print(location, semester, year)

        headers = response.xpath('''
            //table[@class="ui small compact celled table"]
            //th
            /text()
        ''').getall()
        # print(headers)

        sectionData = response.xpath('''
            //table[@class="ui small compact celled table"]
            //td
        ''')
        sectionData.reverse()

        assert len(sectionData) % len(headers) == 0

        while sectionData != []:
            section = {
                'location': location,
                'semester': semester,
                'year': year
            }

            for attribute in self.sectionAttributes:
                header: str = attribute['header']
                key: str = attribute['key']
                default = attribute['default']
                xpath: str = attribute['xpath']
                parseFn = attribute['parseFn']

                if header not in headers:
                    section[key] = default
                    continue

                data: scrapy.Selector = sectionData.pop()

                if xpath is not None:
                    value: str = data.xpath(xpath).get(default=default)

                    if isinstance(value, str):
                        value = value.strip()

                    if value == '':
                        value = None

                    section[key] = value
                elif parseFn is not None:
                    section[key] = parseFn(data)
                else:
                    raise ValueError('Either xpath or parseFn should be present')

            section['crn'] = int(section['crn'])

            # print(section)
            yield section
