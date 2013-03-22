import json

MAX_LEMGTH = 0
FILES = ['salarly_managerjobs.json', 'salarly_pmjobs.json', 'salarly_softwarejobs.json',
'salarly_directorjobs.json', 'salarly_marketingjobs.json', 'salarly_salesjobs.json']

MAX_CITY = 0
MAX_COMPANY = 0
MAX_TITLE = 0
NUM_RECORDS = 0
for f in FILES:
	json_data=open(f)
	print('reading ' + f + '...')
	data = json.load(json_data)

	for job in data:
		NUM_RECORDS = NUM_RECORDS + 1
		city = len(job['city'])
		company = len(job['company'])
		title = len(job['title'])

		if city > MAX_CITY:
			MAX_CITY = city
		if company > MAX_COMPANY:
			MAX_COMPANY = company
		if title > MAX_TITLE:
			MAX_TITLE = title
	json_data.close()

print('maxes out of: ' + str(NUM_RECORDS))
print('max city length: ' + str(MAX_CITY))
print('max company length: ' + str(MAX_COMPANY))
print('max title length: ' + str(MAX_TITLE))