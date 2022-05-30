import csv

with open("second_revised_CSVs/party_majority.csv", mode='w', newline='') as file, open(
        "second_revised_CSVs/chamber_start.csv", mode='r') as fileTwo:
    writer = csv.writer(file, delimiter=',', quotechar='"')
    reader = csv.reader(fileTwo, delimiter=',', quotechar='"')
    for row in reader:
        if not row[0] == "bill_number":
            majority_party = ""
            dem_over_total = 0
            democrats = int(row[11])
            republicans = int(row[12])
            if democrats + republicans == 0:
                dem_over_total = 0
            else:
                dem_over_total = democrats / (democrats + republicans)
            if democrats > republicans:
                majority_party = "Democrats"
            elif republicans > democrats:
                majority_party = "Republicans"
            else:
                majority_party = "No Majority Party"
            row.append(majority_party)
            row.append(dem_over_total)
            writer.writerow(row)
        else:
            columns = ["bill_number", "bill_link", "bill_name", "current_status",
                       "first_house_progress", "second_house_progress", "after_passage_progress", "description",
                       "sponsors", "requester", "bill_history", "democrat_sponsor_count", "republican_sponsor_count",
                       "total_days_spent", "season_years_active", "simplified_status", "current_chamber", "bill",
                       "chambers_visited", "chambers_visited_abbreviated", "number_chambers_visited",
                       "number_filled_in_dots", "chamber_start", "majority_party", "dem_over_total"]
            writer.writerow(columns)