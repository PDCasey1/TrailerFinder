import csv
import ast


with open('data_sets/master_race_attendance.csv', 'r', newline='') as rf:
    reader = csv.DictReader(rf)

    for row in reader:
        if len(ast.literal_eval((row['races_attended']))) < 5:
            pass

        else:
            with open('data_sets/race_attendance.csv', 'a', newline='') as wf:
                writer = csv.DictWriter(wf, fieldnames=['club_name','races_attended'])

                writer.writerow(row)