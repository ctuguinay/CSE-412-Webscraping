import csv
import re
import datetime


def month_to_number(month):
    datetime_object = datetime.datetime.strptime(month, "%b")
    month_number = int(datetime_object.month)
    return month_number


with open("second_revised_CSVs/temporal.csv", mode='w', newline='') as file, open(
        "second_revised_CSVs/second_revised.csv", mode='r') as fileTwo:
    writer = csv.writer(file, delimiter=',', quotechar='"')
    reader = csv.reader(fileTwo, delimiter=',', quotechar='"')
    for row in reader:
        if not row[0] == "bill_number":
            total_days_spent = None
            season_years_active = None
            bill_history = row[10]
            if "2021" in bill_history and "2022" in bill_history:
                split = bill_history.split(".")
                first = split[0]
                last = split[len(split) - 2]
                start_date = re.search("Start (.*) End", first).group(1).split()
                end_date = re.search("End (.*)", last).group(1).split()
                if start_date[0] == "Dec":
                    start_date.append("2020")
                else:
                    start_date.append("2021")
                if end_date[0] == "Dec":
                    end_date.append("2021")
                else:
                    end_date.append("2022")
                start_datetime = datetime.datetime(int(start_date[2]), month_to_number(start_date[0]),
                                                   int(start_date[1]))
                end_datetime = datetime.datetime(int(end_date[2]), month_to_number(end_date[0]), int(end_date[1]))
                difference = end_datetime - start_datetime
                difference = str(difference)
                if difference == "0:00:00":
                    total_days_spent = 0
                else:
                    total_days_spent = int(difference.split(" days")[0])
                season_years_active = "2021-2022"
            elif "2021" in bill_history and "2022" not in bill_history:
                split = bill_history.split(".")
                first = split[0]
                last = split[len(split) - 2]
                start_date = re.search("Start (.*) End", first).group(1).split()
                end_date = re.search("End (.*)", last).group(1).split()
                if start_date[0] == "Dec":
                    start_date.append("2020")
                else:
                    start_date.append("2021")
                if end_date[0] == "Dec":
                    end_date.append("2020")
                else:
                    end_date.append("2021")
                start_datetime = datetime.datetime(int(start_date[2]), month_to_number(start_date[0]),
                                                   int(start_date[1]))
                end_datetime = datetime.datetime(int(end_date[2]), month_to_number(end_date[0]), int(end_date[1]))
                difference = end_datetime - start_datetime
                difference = str(difference)
                if difference == "0:00:00":
                    total_days_spent = 0
                else:
                    total_days_spent = int(difference.split(" days")[0])
                season_years_active = "2021"
            elif "2021" not in bill_history and "2022" in bill_history:
                split = bill_history.split(".")
                first = split[0]
                last = split[len(split) - 2]
                start_date = re.search("Start (.*) End", first).group(1).split()
                end_date = re.search("End (.*)", last).group(1).split()
                if start_date[0] == "Dec":
                    start_date.append("2021")
                else:
                    start_date.append("2022")
                if end_date[0] == "Dec":
                    end_date.append("2021")
                else:
                    end_date.append("2022")
                start_datetime = datetime.datetime(int(start_date[2]), month_to_number(start_date[0]),
                                                   int(start_date[1]))
                end_datetime = datetime.datetime(int(end_date[2]), month_to_number(end_date[0]), int(end_date[1]))
                difference = end_datetime - start_datetime
                difference = str(difference)
                if difference == "0:00:00":
                    total_days_spent = 0
                else:
                    total_days_spent = int(difference.split(" days")[0])
                season_years_active = "2022"

            row.append(total_days_spent)
            row.append(season_years_active)
            writer.writerow(row)
        else:
            columns = ["bill_number", "bill_link", "bill_name", "current_status",
                       "first_house_progress", "second_house_progress", "after_passage_progress", "description",
                       "sponsors", "requester", "bill_history", "democrat_sponsor_count", "republican_sponsor_count",
                       "total_days_spent", "season_years_active"]
            writer.writerow(columns)
