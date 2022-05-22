import csv

with open("second_revised_CSVs/chambers_visited.csv", mode='w', newline='') as file, open(
        "second_revised_CSVs/status_simplify.csv", mode='r') as fileTwo:
    writer = csv.writer(file, delimiter=',', quotechar='"')
    reader = csv.reader(fileTwo, delimiter=',', quotechar='"')
    for row in reader:
        if not row[0] == "bill_number":
            bill_number = int(row[0])
            chambers_visited = ""
            chambers_visited_abbreviated = ""
            number_chambers_visited = 0
            bill_history = row[10]
            split_history = bill_history.split(":")
            for i in range(len(split_history) - 1):
                split = split_history[i]
                number_chambers_visited = number_chambers_visited + 1
                if "SESSION" in split:
                    if bill_number < 5000:
                        chambers_visited = chambers_visited + "HOUSE "
                        chambers_visited_abbreviated = chambers_visited_abbreviated + "H "
                    else:
                        chambers_visited = chambers_visited + "SENATE "
                        chambers_visited_abbreviated = chambers_visited_abbreviated + "S "
                elif "HOUSE" in split:
                    chambers_visited = chambers_visited + "HOUSE "
                    chambers_visited_abbreviated = chambers_visited_abbreviated + "H "
                elif "SENATE" in split:
                    chambers_visited = chambers_visited + "SENATE "
                    chambers_visited_abbreviated = chambers_visited_abbreviated + "S "
                elif "OTHER THAN" in split:
                    chambers_visited = chambers_visited + "GOVERNOR "
                    chambers_visited_abbreviated = chambers_visited_abbreviated + "G "
            chambers_visited = chambers_visited.strip()
            chambers_visited_abbreviated = chambers_visited_abbreviated.strip()
            row.append(chambers_visited)
            row.append(chambers_visited_abbreviated)
            row.append(number_chambers_visited)
            writer.writerow(row)
        else:
            columns = ["bill_number", "bill_link", "bill_name", "current_status",
                       "first_house_progress", "second_house_progress", "after_passage_progress", "description",
                       "sponsors", "requester", "bill_history", "democrat_sponsor_count", "republican_sponsor_count",
                       "total_days_spent", "season_years_active", "simplified_status", "current_chamber", "bill",
                       "chambers_visited", "chambers_visited_abbreviated", "number_chambers_visited"]
            writer.writerow(columns)