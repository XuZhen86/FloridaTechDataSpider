import json
import re

if __name__ == '__main__':
    sections: list = json.load(open('_section.raw.json', 'r'))

    requirements = set()
    for section in sections:
        description: str = section['title'][1]

        try:
            startIndex = re.search(r'\(Requirement[s]?: ', description).end()

            nestingLevel = 1
            for offset, char in enumerate(description[startIndex:]):
                if char == '(':
                    nestingLevel += 1
                elif char == ')':
                    nestingLevel -= 1

                if nestingLevel == 0:
                    endIndex = startIndex + offset
                    break

            requirements.add(description[startIndex:endIndex])
        except AttributeError:
            pass

    requirements = list(requirements)
    requirements.sort()

    json.dump(requirements, open('requirement.json', 'w'), indent=4)
    json.dump(requirements, open('requirement.min.json', 'w'), separators=(',', ':'))
