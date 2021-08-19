
# The function below generates a dictionary of clubs and the race ID's that they
# attended. It reads 'MASTER_DATA.CSV' for the appropriate information, and
# then feeds it to 'club_attendance.csv'. Takes some  time to run, so unless you
# really need to, it's best just to use the pre-generated club_attendance.csv file.

import csv
import ast

def attendence_gen():

    data_set_length = None
    clubs = set()

    with open('MASTER_DATA.csv', newline='') as f:
        # This first 'with' statement finds the length of "MASTER_DATA.csv"
        # for use in a printed counter in the rest of the function.

        reader = csv.DictReader(f)
        data_set_length = len(list(reader))

    with open('MASTER_DATA.csv', newline='') as f:
        # Generates unique club name set
        
        reader = csv.DictReader(f)
        
        for count, row in enumerate(reader):
            for i in ast.literal_eval(row['clubs']):
                clubs.add(i[0])
            
            print('Row {} of {} processed.'.format(count+1, data_set_length))


    for count, club in enumerate(clubs):

        # Goes through each line in 'MASTER_DATA.csv' and checks each entry
        # for the current club name. If it finds it, appends the corresponding
        # 'race_ID' to the 'club_attendance' variable and immediately stop
        # checking that row for the entry (any further checks would yield nothing,
        # since clubs are only represented once for each race).
        
        with open('MASTER_DATA.csv', newline='') as rf:
            reader = csv.DictReader(rf)
            
            print(f'{count+1} of {len(clubs)} clubs processing')
            print(f'Working on {club}...')
            attended = []
            
            for row in reader:
                for entry in ast.literal_eval(row['clubs']):

                    if entry[0] != club:
                        continue
                    else: 
                        attended.append(row['event_ID'])
                        break

                club_attendance = {
                'club_name': club,
                'races_attended': attended
                }
                

            with open('club_attendance.csv', 'a') as wf:
                writer = csv.DictWriter(wf, fieldnames = ['club_name', 'races_attended'])
                writer.writerow(club_attendance)