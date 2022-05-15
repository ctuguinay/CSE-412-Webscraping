import csv

with open("second_revised_CSVs/status_simplify.csv", mode='w', newline='') as file, open(
        "second_revised_CSVs/temporal.csv", mode='r') as fileTwo:
    writer = csv.writer(file, delimiter=',', quotechar='"')
    reader = csv.reader(fileTwo, delimiter=',', quotechar='"')
    for row in reader:
        if not row[0] == "bill_number":
            simplified_status = ""
            current_chamber = ""
            status = row[3]
            if status[0] == "H":
                current_chamber = "Representatives"
            elif status[0] == "S":
                current_chamber = "Senators"
            else:
                current_chamber = "Neither"
            if "C" == status[0]:
                simplified_status = "Law"
            elif "Gov vetoed" in status:
                simplified_status = "Governor Veto"
            elif "Rules X" in status:
                simplified_status = "Rules X"
            elif "Rules" in status and "Rules X" not in status:
                simplified_status = "Rules Committee"
            else:
                simplified_status = "Non-Rules Committee"
            row.append(simplified_status)
            row.append(current_chamber)
            writer.writerow(row)
        else:
            columns = ["bill_number", "bill_link", "bill_name", "current_status",
                       "first_house_progress", "second_house_progress", "after_passage_progress", "description",
                       "sponsors", "requester", "bill_history", "democrat_sponsor_count", "republican_sponsor_count",
                       "total_days_spent", "season_years_active", "simplified_status", "current_chamber"]
            writer.writerow(columns)