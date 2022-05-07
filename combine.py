from os import listdir
import csv

topics = listdir("topic_CSVS")

dataset = []
combined = "combined_topics.csv"
for topic in topics:
    filename = "topic_CSVS/" + topic
    with open(filename, 'r', newline='') as csvFile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for row in reader:
            dataset.append(row)

with open(combined, 'w', newline='') as combinedFile:
    writer = csv.writer(combinedFile, delimiter=',', quotechar='"')
    for data in dataset:
        writer.writerow(data)

members = listdir("member_CSVS")

dataset = []
combined = "combined_members.csv"
for member in members:
    filename = "member_CSVs/" + member
    with open(filename, 'r', newline='') as csvFile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for row in reader:
            if member == "representatives.csv":
                row.append("representative")
            else:
                row.append("senator")
            dataset.append(row)

with open(combined, 'w', newline='') as combinedFile:
    writer = csv.writer(combinedFile, delimiter=',', quotechar='"')
    for data in dataset:
        writer.writerow(data)


