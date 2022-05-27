import csv

with open("second_revised_CSVs/chamber_start.csv", mode='w', newline='') as file, open(
        "second_revised_CSVs/chambers_visited.csv", mode='r') as fileTwo:
    writer = csv.writer(file, delimiter=',', quotechar='"')
    reader = csv.reader(fileTwo, delimiter=',', quotechar='"')
    for row in reader:
        if not row[0] == "bill_number":
            bill_number = int(row[0])
            if bill_number < 5000:
                chamber = "House"
            else:
                chamber = "Senate"
            row.append(chamber)
            writer.writerow(row)
        else:
            columns = ["bill_number", "bill_link", "bill_name", "current_status",
                       "first_house_progress", "second_house_progress", "after_passage_progress", "description",
                       "sponsors", "requester", "bill_history", "democrat_sponsor_count", "republican_sponsor_count",
                       "total_days_spent", "season_years_active", "simplified_status", "current_chamber", "bill",
                       "chambers_visited", "chambers_visited_abbreviated", "number_chambers_visited",
                       "number_filled_in_dots", "chamber_start"]
            writer.writerow(columns)