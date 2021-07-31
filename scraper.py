from bs4 import BeautifulSoup
from IPython.display import clear_output
import requests
import re
import csv

labels = ['event_ID', 'event_name', 'event_location', 'event_date', 'clubs']

with open('dataset.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames = labels)
    writer.writeheader()

def sort_club_data():
    
    club_list = []
    for count, i in enumerate(club_data):

        if count % 6 == 0:
            club_list.append(club_data[count:count+6])
            
    return club_list

error_id = []

for i in range(1,7501):
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
        
        raw_club_data = soup.find('table', id = 'teamList').text
        club_data = re.split(r'\s\s\s+,?|\n', raw_club_data)[7:-1]
        date = soup.find('li', {'class': "rc-regatta-dates"}).text.strip()
        location = soup.find('li', {'itemprop': "location"}).text
        
        event_ID = str(job_id)
        event_name = soup.h2.text
        event_date = re.sub(r'\n+\t+', '', date).strip()
        event_location = re.sub(r'\s\s+', '', location).replace('(', ', ').rstrip('())')
        
        dataset['event_ID'] = job_id
        dataset['event_name'] = event_name
        dataset['event_location'] = event_location
        dataset['event_date'] = event_date
        dataset['clubs'] = sort_club_data()
                
        with open('dataset.csv', 'a') as f:
            writer = csv.DictWriter(f, fieldnames = labels)
            writer.writerow(dataset)

        print('Data Found!\n{} of 7500 processed.'.format(i))
        clear_output(wait=True)
        
    except:
        error_id.append(i)
        print('Data Not Found.\n{} of 7500 processed.'.format(i))
        clear_output(wait=True)