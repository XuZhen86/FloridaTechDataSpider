import json
from dataclasses import asdict, astuple, dataclass, fields


@dataclass
class Tag:
    code: str
    name: str

    def __lt__(self, t):
        return self.code < t.code


# https://catalog.fit.edu/content.php?catoid=9&navoid=367
presetTags = [
    ['CC', 'Cross-cultural'],
    ['CL', 'Computer Literacy Requirement'],
    ['COM', 'Communication Elective'],
    ['HON', 'Honors Sections'],
    ['HU', 'Humanities Elective'],
    ['LA', 'Liberal Arts Elective'],
    ['Q', 'Scholarly Inquiry Requirement'],
    ['SS', 'Social Science Elective']
]

if __name__ == '__main__':
    tags = [
        Tag(code=presetTag[0], name=presetTag[1])
        for presetTag in presetTags
    ]

    tags.sort()

    keys = [f.name for f in fields(Tag)]
    values = [list(astuple(t)) for t in tags]

    json.dump(
        [asdict(t) for t in tags],
        open('tag.json', 'w'),
        indent=4
    )
    json.dump(
        {'keys': keys, 'values': values},
        open('tag.min.json', 'w'),
        separators=(',', ':')
    )
