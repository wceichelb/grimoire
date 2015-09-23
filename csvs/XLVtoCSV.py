import os
import csv

def fix_csv(filename):
    with open(filename) as f:
        target = filename[:-4] + "2.csv"
        with open(target, "wb") as ff:
            writer = csv.writer(ff)
            content = csv.reader(f, delimiter=';')
            new_content = []
            for entry in content:
                new_entry = []
                for line in entry:
                    if "," in line:
                        new_line = ("{0}").format(line)
                    else:
                        new_line = line
                    new_entry.append(new_line)
                writer.writerow(new_entry)


for file in os.listdir(os.getcwd()):
    if '.csv' in file:
        print file
        fix_csv(file)
