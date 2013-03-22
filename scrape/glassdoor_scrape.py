from bs4 import BeautifulSoup
import urllib2
import re
import json
import ast

JOB_QUERY_TO_NAME = {'software+engineer':'softwarejobs',
		'product+manager':'pmjobs',
		'sales':'salesjobs',
		'marketing':'marketingjobs',
		'manager':'managerjobs',
		'director':'directorjobs'
		}
BASE_URL = 'http://www.salar.ly'
JOBS_URL = 'http://www.salar.ly/salaries/?'

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


def clean_print_output(jobstr, current_job):

	jobstr = ','.join(jobstr)
	joblist = '[' + jobstr + ']'
	
	joblist = re.sub('"', '\'', joblist)
	joblist = re.sub('{\'', '{"', joblist)
	joblist = re.sub('\':', '":', joblist)
	joblist = re.sub('": \'', '": "', joblist)
	joblist = re.sub('\',', '",', joblist)
	joblist = re.sub(', \'', ', "', joblist)
	joblist = re.sub('\'}', '"}', joblist)
	#special cases
	joblist = re.sub('kor"', 'kor\'', joblist)
	print('Output = ' + joblist)
	#print joblist

	outfile = open('salarly_' +  JOB_QUERY_TO_NAME[current_job] + '.json', 'ab+')
	jsonobj = json.loads(joblist)
	pretty_result = json.dump(jsonobj, outfile, sort_keys=True)
	outfile.flush()
	outfile.close()

def scrape_top_level():
	#pages
	def create_page_ranges():

		eng_pages = range(1,71)
		pm_pages = range(1,7)
		sales_pages = range(1,11)
		marketing_pages = range(1,12)

		manager_pages = range(1,70)
		director_pages = range(1,21)
		jobpages = {}

		jobpages['software+engineer'] = eng_pages
		jobpages['product+manager'] = pm_pages
		jobpages['sales'] = sales_pages
		jobpages['marketing'] = marketing_pages

		jobpages['manager'] = manager_pages
		jobpages['director'] = director_pages
		return jobpages

	def create_page_append(page):
		return '&page=' + str(page)

	def create_title_append(title):
		return '&title=' + title	

	jobpages = create_page_ranges()
	for entry in jobpages:
		CUR_JOB = entry
		pages = jobpages[CUR_JOB]
		print('Querying for ' + CUR_JOB)
		jobstr = []
		for page in pages:
			#get the url for job urls
			req_obj = urllib2.urlopen(JOBS_URL + create_title_append(CUR_JOB)
				+ create_page_append(page) ).read()
			if not req_obj:
				continue

			#soupify!
			soup = BeautifulSoup(req_obj)
			if not soup:
				continue

			#obtain embedded json
			tooltip = re.search('\[\{.*\}\];',soup.get_text()).group(0)
			jinfo = str(tooltip)[1:len(tooltip)-2]
			jobstr.append(jinfo)

		#clean output and write
		clean_print_output(jobstr, CUR_JOB)

		

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




