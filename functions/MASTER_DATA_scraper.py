# ------------------------------------------------------------------------------
# Webscraper that builds 'MASTER_DATA.csv'. Scrapes regattacentral.com for 
# relevant event information. Currently not automated, but I'd like to add 
# functionaity that checks all pages periodically whose 'event_date' has not 
# passed, or has passed no longer than a few days prior.

# This does not update MASTER_DATA.csv, only generates it initially. The 
# updater, when created, will ignore old races and focus only on upcoming ones.
# ------------------------------------------------------------------------------


from bs4 import BeautifulSoup
import requests
import re
import csv

# from IPython.display import clear_output
# clear_output is nice for debugging, only relevant in a Jupyter Notebook
# environment (Along with commented-out commands below.)

labels = ['event_ID', 'event_name', 'event_location', 'event_date', 'clubs']

def write_header(): # initiated only once to write header for MASTER_DATA.csv 
    with open('MASTER_DATA.csv', 'w') as f: 
        writer = csv.DictWriter(f, fieldnames = labels)
        writer.writeheader()

def scrape_regatta_central():
    
    error_id = [] # list of job_id's that threw an error when run.

    def sort_club_data(): # splits club_data into indiviual clubs' properties.
    
        club_list = []
        for count, i in enumerate(club_data):

            if count % 6 == 0:
                club_list.append(club_data[count:count+6])
                
        return club_list

    for i in range(7500):
        
        # as of this writing, the highest job_id on regattacentral.com is
        # 7441. Haven't figured out a way to autodetect this highest
        # number reliably yet.

        URL = 'https://www.regattacentral.com/regatta/clubs/?job_id='
        job_id = i
        website = requests.get(URL+str(job_id)).text
        soup = BeautifulSoup(website, 'lxml')

        try:
            dataset = {
                'event_ID':None,
                'event_name':None,
                'event_location':None,
                'event_date':None,
                'clubs':None,
            }
            
            # extract the club data as _raw_club_data, and then split that
            # into the more workable club_data, which is chopped up by 
            # sort_club_data into each individual program. Also, extract
            # date and location of race.

            raw_club_data = soup.find('table', id = 'teamList').text
            club_data = re.split(r'\s\s\s+,?|\n', raw_club_data)[7:-1]
            date = soup.find('li', {'class': "rc-regatta-dates"}).text.strip()
            location = soup.find('li', {'itemprop': "location"}).text
            
            event_ID = str(job_id)
            event_name = soup.h2.text
            event_location = re.sub(r'\s\s+', '', location).replace('(', ', ').rstrip('())')
            event_date = re.sub(r'\n+\t+', '', date).strip()
            
            dataset['event_ID'] = event_ID
            dataset['event_name'] = event_name
            dataset['event_location'] = event_location
            dataset['event_date'] = event_date
            dataset['clubs'] = sort_club_data()
                    
            with open('MASTER_DATA.csv', 'a') as f:
                writer = csv.DictWriter(f, fieldnames = labels)
                writer.writerow(dataset)

            print('Data Found!\n{} of 7500 processed.'.format(i))
            # clear_output(wait=True)
            
        except:
            error_id.append(i)
            print('Data Not Found.\n{} of 7500 processed.'.format(i))
            # clear_output(wait=True)

