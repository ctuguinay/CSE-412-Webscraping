from bs4 import BeautifulSoup
from requests_html import HTMLSession
import csv

with HTMLSession() as session:

    with open("second_revised_CSVs/second_revised.csv", mode='a') as file:

        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        #columns = ["bill_number", "bill_link", "bill_name", "current_status",
        #           "first_house_progress", "second_house_progress", "after_passage_progress", "description_2",
        #           "sponsors", "requester", "bill_history"]

        #csv_writer.writerow(columns)

        #for number in list(range(1284, 4000)) + list(range(5000, 8000)):

        for number in list(range(1000, 4000)) + list(range(5000, 8000)):

        #for number in [3998, 3999]:

            url = "https://app.leg.wa.gov/billsummary?BillNumber=" + str(number) + "&Year=2021&Initiative=false"

            bill = [number, url]

            response = session.get(url)
            response.html.render()
            soup = BeautifulSoup(response.html.html, "html.parser")

            clearfix_rows = soup.find(id="pageContent").find_all("div", class_="row clearfix")
            count = 0
            for row in clearfix_rows:
                if "Bill Not Found." in row.text:
                    count = count + 1

            if not count > 0:
                bill_name = soup.find_all("div", class_="billStatusAtAGlanceSubText")[0].text
                current_status = soup.find_all("div", class_="billStatusAtAGlanceSubText")[1].text
                current_status = current_status.strip()
                bill.append(bill_name)
                bill.append(current_status)
                div = soup.find(id="horizontalStatusDisplay").find("div", class_="col-xs-12")
                svgs = div.find_all("svg")[1:4]
                for svg in svgs:
                    circles = []
                    circle_set = svg.find_all("circle")
                    polyline_set = svg.find_all("polyline")
                    if len(circle_set) == 5:
                        circles = ["1", "0", "0", "0"]
                    elif len(circles) == 1:
                        circles = ["1", "1", "1", "1"]
                    elif len(circle_set) == 7 and len(polyline_set) == 3:
                        circles = ["1", "1", "1", "1"]
                    elif len(circle_set) == 7 and len(polyline_set) == 2:
                        circles = ["1", "1", "1", "0"]
                    elif len(circle_set) == 4:
                        circles = ["0", "0", "0", "0"]
                    bill.append(circles)
                div = soup.find("div", class_="container-fluid").find("div", class_="row clearfix").findChildren("div",class_=None)[5]
                divs = div.find_all("div", class_="row clearfix")
                try:
                    bill.append(divs[1].text.strip())
                except:
                    bill.append("No Description")
                try:
                    bill.append((" ".join(divs[2].text.split()).replace("Sponsors: ", "")))
                except:
                    bill.append("No Sponsors")
                try:
                    if "Companion Bill:" in divs[3].text.strip():
                        bill.append("No Requester")
                    else:
                        bill.append(divs[3].text.strip().replace("\n", " ").replace("By Request: ", ""))
                except:
                    bill.append("No Requester")
                bill_history = soup.find("div", class_="col-xs-12 col-csm-11 col-sm-10 col-md-9 col-lg-10")
                p_list = bill_history.find_all("p")
                history_table_list = bill_history.find_all("div", class_="historytable")
                string = ""
                for index in range(len(p_list)):
                    p = p_list[index]
                    step = p.text.strip()
                    history_table = history_table_list[index]
                    dates = history_table.find_all("div", class_="historyrow")
                    first_date = dates[0].text
                    last_date = ""
                    count = 1
                    while True:
                        if not dates[len(dates) - count].text.strip():
                            count = count + 1
                        else:
                            last_date = dates[len(dates) - count].text.strip()
                            break
                    first_date = first_date.strip()
                    last_date = last_date.strip()
                    string = string + step + ": Start " + first_date + " End " + last_date + ". "
                string = string.strip()
                bill.append(string)
                response.close()
                print(bill)
                csv_writer.writerow(bill)
