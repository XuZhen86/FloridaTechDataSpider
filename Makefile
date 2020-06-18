all: metaData.py building.min.json course3.min.json description.min.json note.min.json restriction.min.json session.min.json title.min.json campus.min.json courseAttribute.min.json employee.min.json prerequisite.min.json scheduleType.min.json subject.min.json department.min.json level.min.json requirement.min.json section.min.json tag.min.json
	python3 metaData.py
	mkdir -p dist
	rm -f dist/*
	cp metaData.min.json building.min.json course3.min.json description.min.json note.min.json restriction.min.json session.min.json title.min.json campus.min.json courseAttribute.min.json employee.min.json prerequisite.min.json scheduleType.min.json subject.min.json department.min.json level.min.json requirement.min.json section.min.json tag.min.json dist

clean:
	rm -f *.json

SCRAPY_OPTIONS=-s LOG_LEVEL=WARNING -s CLOSESPIDER_ERRORCOUNT=1

_department.raw.json: FloridaTechDataSpider/spiders/department_spider.py formatJson.py
	> _department.raw.json
	scrapy crawl department -o _department.raw.json ${SCRAPY_OPTIONS}
	python3 formatJson.py _department.raw.json

_employee.raw.json: FloridaTechDataSpider/spiders/employee_spider.py formatJson.py
	> _employee.raw.json
	scrapy crawl employee -o _employee.raw.json ${SCRAPY_OPTIONS}
	python3 formatJson.py _employee.raw.json

_section.raw.json: FloridaTechDataSpider/spiders/section_spider.py formatJson.py
	> _section.raw.json
	scrapy crawl section -o _section.raw.json ${SCRAPY_OPTIONS}
	python3 formatJson.py _section.raw.json

_pawsCourse.raw.json: FloridaTechDataSpider/spiders/pawsCourse_spider.py course.json formatJson.py
	> _pawsCourse.raw.json
	scrapy crawl pawsCourse -o _pawsCourse.raw.json ${SCRAPY_OPTIONS}
	python3 formatJson.py _pawsCourse.raw.json

_pawsSection.raw.json: FloridaTechDataSpider/spiders/pawsSection_spider.py _section.raw.json formatJson.py
	> _pawsSection.raw.json
	scrapy crawl pawsSection -o _pawsSection.raw.json ${SCRAPY_OPTIONS}
	python3 formatJson.py _pawsSection.raw.json

_pawsBuilding.raw.json: FloridaTechDataSpider/spiders/pawsBuilding_spider.py course.json _pawsSection.raw.json formatJson.py
	> _pawsBuilding.raw.json
	scrapy crawl pawsBuilding -o _pawsBuilding.raw.json ${SCRAPY_OPTIONS}
	python3 formatJson.py _pawsBuilding.raw.json


tag.json tag.min.json: tag.py
	python3 tag.py

campus.json campus.min.json: campus.py _pawsSection.raw.json
	python3 campus.py

note.json note.min.json: note.py _pawsSection.raw.json
	python3 note.py

requirement.json requirement.min.json: requirement.py _pawsSection.raw.json
	python3 requirement.py

session.json session.min.json: session.py _pawsSection.raw.json
	python3 session.py

title.json title.min.json: title.py _pawsSection.raw.json
	python3 title.py

building.json building.min.json: building.py _department.raw.json _employee.raw.json _pawsBuilding.raw.json
	python3 building.py

department.json department.min.json: department.py _department.raw.json building.json
	python3 department.py

description.json description.min.json: description.py _pawsSection.raw.json requirement.json tag.json
	python3 description.py

employee.json employee.min.json: employee.py _employee.raw.json building.json department.json _pawsSection.raw.json
	python3 employee.py

course.json course.min.json: course.py _pawsSection.raw.json campus.json description.json tag.json title.json
	python3 course.py


level.json level.min.json: level.py _pawsCourse.raw.json
	python3 level.py

scheduleType.json scheduleType.min.json: scheduleType.py _pawsCourse.raw.json
	python3 scheduleType.py

courseAttribute.json courseAttribute.min.json: courseAttribute.py _pawsCourse.raw.json
	python3 courseAttribute.py

restriction.json restriction.min.json: restriction.py _pawsCourse.raw.json _pawsSection.raw.json
	python3 restriction.py

prerequisite.json prerequisite.min.json: prerequisite.py _pawsCourse.raw.json _pawsSection.raw.json
	python3 prerequisite.py

course2.json course2.min.json: course2.py _pawsCourse.raw.json level.json scheduleType.json restriction.json prerequisite.json courseAttribute.json
	python3 course2.py

section.json section.min.json: section.py building.json campus.json course2.json description.json employee.json note.json session.json title.json level.json restriction.json prerequisite.json _pawsSection.raw.json
	python3 section.py

subject.json subject.min.json: subject.py course2.json
	python3 subject.py

course3.json course3.min.json: course3.py subject.json course2.json
	python3 course3.py
