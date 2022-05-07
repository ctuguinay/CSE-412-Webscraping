from tempfile import NamedTemporaryFile
from os import listdir
import shutil
import csv

topics = listdir("topic_CSVS")

for topic in topics:
    filename = "topic_CSVS/" + topic
    tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

    with open(filename, 'r', newline='') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        writer = csv.writer(tempfile, delimiter=',', quotechar='"')

        for row in reader:
            if len(row) == 11:
                writer.writerow(row)

    shutil.move(tempfile.name, filename)

members = listdir("member_CSVS")

for member in members:
    filename = "member_CSVS/" + member
    tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

    with open(filename, 'r', newline='') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        writer = csv.writer(tempfile, delimiter=',', quotechar='"')

        for row in reader:
            if len(row) == 2:
                writer.writerow(row)

    shutil.move(tempfile.name, filename)