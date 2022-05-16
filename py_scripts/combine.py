from os import listdir
import csv

topics = listdir("topic_CSVS")

dataset = []
count = 0
combined = "topic_CSVs/combined_topics.csv"
for topic in topics:
    filename = "topic_CSVS/" + topic
    with open(filename, 'r', newline='') as csvFile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for row in reader:
            if row[0] == "main_topic" and count == 0:
                count = count + 1
                dataset.append(row)
            elif not row[0] == "main_topic":
                dataset.append(row)

with open(combined, 'w', newline='') as combinedFile:
    writer = csv.writer(combinedFile, delimiter=',', quotechar='"')
    for data in dataset:
        writer.writerow(data)

members = listdir("member_CSVS")

dataset = []
combined = "member_CSVs/combined_members.csv"
count = 0
for member in members:
    filename = "member_CSVs/" + member
    with open(filename, 'r', newline='') as csvFile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for row in reader:
            if row[0] == "name" and count == 0:
                count = count + 1
                row.append("member_type")
                dataset.append(row)
            elif not row[0] == "name":
                if member == "representatives.csv":
                    row.append("representative")
                else:
                    row.append("senator")
                dataset.append(row)

with open(combined, 'w', newline='') as combinedFile:
    writer = csv.writer(combinedFile, delimiter=',', quotechar='"')
    for data in dataset:
        writer.writerow(data)


