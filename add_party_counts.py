from tempfile import NamedTemporaryFile
from os import listdir
import shutil
import csv

topics = listdir("topic_CSVS")

filenameTwo = "member_CSVs/combined_members.csv"
for topic in topics:
    filename = "topic_CSVS/" + topic
    print(topic)
    tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

    with open(filename, 'r', newline='') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        writer = csv.writer(tempfile, delimiter=',', quotechar='"')
        # columns = ["main_topic", "description_1", "bill_link", "bill_name", "current_status", "house_progress",
        #           "senate_progress", "after_passage_progress", "description_2", "sponsors", "requester"]
        # writer.writerow(columns)
        for row in reader:
            if "main_topic" == row[0]:
                row[11] = "democrat_sponsor_count"
                row[12] = "republican_sponsor_count"
                writer.writerow(row)
            else:
                sponsors = row[9]
                d_count = 0
                r_count = 0
                with open(filenameTwo, 'r', newline='') as csvFileTwo:
                    reader_two = csv.reader(csvFileTwo, delimiter=',', quotechar='"')
                    for row_two in reader_two:
                        if not "name" == row_two[0]:
                            name = row_two[0]
                            party = row_two[1]
                            last_name = name.split()[1]
                            if name in sponsors or last_name in sponsors:
                                # print(name)
                                # print(last_name)
                                # print(sponsors)
                                if "R" in party:
                                    r_count = r_count + 1
                                    # print(r_count)
                                elif "D" in party:
                                    d_count = d_count + 1

                row[11] = d_count
                row[12] = r_count
                writer.writerow(row)

    shutil.move(tempfile.name, filename)
