from bs4 import BeautifulSoup
import urllib2
import re
import json
import ast

LOCATIONS = ['California']
JOBS = ['engineer', 'product+manager']
JOB_CATEGORIES = ['Employer Name', 'Start Date', 'City of Job Location', 'Job Title',
'State of Job Location', 'Prevailing Wage Rate', 'Wage Unit']

BASE_URL = 'http://www.salar.ly'
JOBS_URL = 'http://www.salar.ly/salaries/?'
CUR_JOB = 'marketing'

jobstr = []

def scrape_job_record(job_path):
	req_obj = urllib2.urlopen(BASE_URL + job_path).read()
	soup = BeautifulSoup(req_obj)
	job_json = {}

	#et all the tr/td tags, where data is stored
	tr_tags = soup.find_all('tr')
	if not tr_tags:
		return
	for tr_tag in tr_tags:
		if not tr_tag:
			return

		#get all the tds
		td_tags = tr_tag.children
		if not td_tags:
			return

		#get all the info from all the tags
		for td_tag in td_tags:
			if not td_tag or not td_tag.string:
				continue

			#take all the job information
			if td_tag.string in JOB_CATEGORIES:
				key = td_tag.string
				neighbor = td_tag.next_sibling.next_sibling
				if not neighbor or not neighbor.string:
					continue
				
				#we found a job! put in it in the data
				value = neighbor.string
				job_json[key] = value
	jobs_list.append(job_json)


def scrape_top_level():
	#pages
	eng_pages = range(35,71)
	pm_pages = range(1,7)
	sales_pages = range(1,11)
	marketing_pages = range(1,12)
	def create_page_append(page):
		return '&page=' + str(page)

	def create_title_append(title):
		return '&title=' + title	

	for page in marketing_pages:
		#get the url for job urls
		req_obj = urllib2.urlopen(JOBS_URL + create_title_append(CUR_JOB
			+ create_page_append(page)) ).read()
		if not req_obj:
			continue

		#soupify!
		soup = BeautifulSoup(req_obj)
		if not soup:
			continue

		tooltip = re.search('\[\{.*\}\];',soup.get_text()).group(0)
		jinfo = str(tooltip)[1:len(tooltip)-2]
		jobstr.append(jinfo)


		

		#get all the records
		"""
		jobs_records = soup.find_all('a', target='_blank')
		for anchor in jobs_records:
			if anchor['href'] and anchor['href'].startswith('/case'):
				#parse the records
				#scrape_job_record(anchor['href'])
				continue
		"""


scrape_top_level()


jobstr = ','.join(jobstr)
joblist = '[' + jobstr + ']'

joblist = re.sub('"', '\'', joblist)
joblist = re.sub('{\'', '{"', joblist)
joblist = re.sub('\':', '":', joblist)
joblist = re.sub('": \'', '": "', joblist)
joblist = re.sub('\',', '",', joblist)
joblist = re.sub(', \'', ', "', joblist)
joblist = re.sub('\'}', '"}', joblist)
##oblist = json.JSONDecoder().decode(joblist)



jsonobj = json.loads(joblist)
pretty_result = json.dumps(jsonobj, sort_keys=True, indent=2)
print(pretty_result)

