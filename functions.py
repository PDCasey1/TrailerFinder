import csv
import ast


def create_club_set():
    # returns a set of all clubs found in all races.

    clubs = set([])

    with open('masterdataset.csv', newline='') as f:
        reader = csv.DictReader(f)
        
        for count, row in enumerate(reader):
            for i in ast.literal_eval(row['clubs']):
                    clubs.add(i[0])
                
           # print('Row {} of {} processed.'.format(count, 6197))

    return clubs

def clubs_by_attendance(clubs):
    # returns a dictionary of clubs and the corresponding events they attended by 'event_ID'.

    club_attendance = {}

    with open('masterdataset.csv', newline='') as f:
        reader = csv.DictReader(f)
        
        for clubcount, club in enumerate(clubs):
            
            if clubcount < 9:
                
                attended = []
                print(f'Working on {club}...')

                for row in reader:
                    for entry in ast.literal_eval(row['clubs']):
                        
                        if club in entry:
                            attended.append(row['event_ID'])
                            print(row['event_ID'])
                            break

                        club_attendance[club] = attended


                print(f'{clubcount+1} of {len(clubs)} clubs processed')

    print(club_attendance)

clubs_by_attendance(create_club_set())