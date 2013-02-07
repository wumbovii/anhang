#Scrape angelList and put into JSON format
#
import urllib
import json
import io

COMPANY_FIELDS = ['id', 'name', 'logo_url', 'company_url', 'product_desc', 'high_concept']
COMPANY_PATH = "https://api.angel.co/1/startups/batch?ids="

JOBS_FIELDS = [ 'title', 'updated_at', 'equity_cliff', 'equity_min', 'equity_max', 'salary_min', 'salary_max']
JOBS_PATH = "https://api.angel.co/1/jobs?page="

consolidated_cmpy_data = []
consolidated_jobs_data = []
jobs_skills_count = {}
jobs_roles_count = {}

batch_count = 1
batch_size = 50
max_batch = 500
def create_batch():
  if batch_count == 1:
    return range(1+batch_size*(batch_count-1), batch_size*batch_count)
  return range(batch_size*(batch_count-1), batch_size*batch_count)

def get_cmpy_data(consolidated_cmpy_data):

  def create_cmpy_params(cids):
    return ','.join( map(str, cids) )

  params = create_cmpy_params(create_batch())

  req_obj = urllib.urlopen(COMPANY_PATH + params).read()
  req_json = json.loads(req_obj)
    
  for cmpy in req_json:

    if 'error' in cmpy:
      continue

    if (not 'hidden' in cmpy) or cmpy['hidden'] == True:
      continue

    cmpy_info = {}
    cmpy_id = cmpy['id']

    #basic company info
    for key in COMPANY_FIELDS:
      if key in cmpy:
        cmpy_info[key] = cmpy[key]
    
    #mark tags
    markets_list = []
    if 'markets' in cmpy:
      markets = cmpy['markets']
      for markets_entry in markets:
        if 'display_name' in markets_entry:
          markets_list.append(markets_entry['display_name'])

    #location tags
    locations_list = []
    if 'locations' in cmpy:
      locations = cmpy['locations']
      for location in locations:
        if 'display_name' in location:
          locations_list.append(location['display_name'])

    cmpy_info['markets'] = markets_list
    cmpy_info['locations'] = locations_list
    consolidated_cmpy_data.append(cmpy_info)

def get_jobs_data():

  pages = range(1,98)

  for page in pages:
    req_obj = urllib.urlopen(JOBS_PATH + str(page)).read()
    req_json = json.loads(req_obj)

    #get job info
    if 'error' in req_json:
      continue

    if not 'jobs' in req_json:
      continue

    jobs = req_json['jobs']
    for job in jobs:

      jobs_info = {}
      for key in JOBS_FIELDS:
        if key in job:
          jobs_info[key] = job[key]
        if ('startup' in job) and (job['startup']['hidden'] is not True):
          jobs_info['company'] = job['startup']['name']

      #get skills and roles
      if not 'tags' in job:
        continue
      else:
        tags = job['tags']
      
      skills = []
      roles = []
      for tag in tags:

        if 'tag_type' in tag:    
          #get skills per job          
          if tag['tag_type'] == 'SkillTag':
            skill = tag['display_name']
            skills.append(skill)
            if skill in jobs_skills_count:
              jobs_skills_count[skill] = jobs_skills_count[skill] + 1
            else:
              jobs_skills_count[skill] = 1

          #get roles per job          
          if tag['tag_type'] == 'RoleTag':
            role = tag['display_name']
            roles.append(role)
            if role in jobs_roles_count:
              jobs_roles_count[role] = jobs_roles_count[role] + 1
            else:
              jobs_roles_count[role] = 1
      jobs_info['skills'] = skills
      jobs_info['roles'] = roles
      consolidated_jobs_data.append(jobs_info)
  consolidated_jobs_data.append(jobs_roles_count)
  consolidated_jobs_data.append(jobs_skills_count)


      

  

#company basic infos
while batch_count < max_batch:
  #get cmpy info
  get_cmpy_data(consolidated_cmpy_data)
  batch_count = batch_count + 1

#jobs info
#get_jobs_data()

#print to file
"""
outfile = open('angellist.txt', 'ab+')
pretty_result = json.dump(consolidated_cmpy_data, outfile)
outfile.flush()
outfile.close()
"""
pretty_result = json.dumps(consolidated_cmpy_data, sort_keys=True, indent=2)
print(pretty_result)
