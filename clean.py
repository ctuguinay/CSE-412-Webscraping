from tempfile import NamedTemporaryFile
from os import listdir
import shutil
import csv

# topics = listdir("topic_CSVS")
topics = listdir("second_revised_CSVs")

filenameTwo = "member_CSVs/combined_members.csv"
for topic in topics:
    # filename = "topic_CSVS/" + topic
    filename = "second_revised_CSVs/" + topic
    tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

    with open(filename, 'r', newline='') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        writer = csv.writer(tempfile, delimiter=',', quotechar='"')
        for row in reader:
            if len(row) > 0:
                if not row[0] == "bill_number":
                    sponsors = row[9]
                    sponsors = sponsors.replace("Johnson, J.", "Jesse Johnson")
                    sponsors = sponsors.replace("Wilson, C.", "Claire Wilson")
                    sponsors = sponsors.replace("Wilson, J.", "Jeff Wilson")
                    sponsors = sponsors.replace("Wilson, L.", "Linda Wilson")
                    row[9] = sponsors
                    writer.writerow(row)
                else:
                    columns = ["bill_number", "bill_link", "bill_name", "current_status",
                               "first_house_progress", "second_house_progress", "after_passage_progress", "description",
                               "sponsors", "requester", "bill_history"]
                    writer.writerow(columns)

    shutil.move(tempfile.name, filename)

members = listdir("member_CSVS")

for member in members:
    filename = "member_CSVS/" + member
    tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

    with open(filename, 'r', newline='') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        writer = csv.writer(tempfile, delimiter=',', quotechar='"')

        # columns = ["name", "party"]
        # writer.writerow(columns)

        for row in reader:
            writer.writerow(row)

    shutil.move(tempfile.name, filename)
