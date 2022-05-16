from bs4 import BeautifulSoup
from requests_html import HTMLSession
import csv

totalData = None
h3 = None
first_span = None

topics = ["?biennium=2021-22&topic=COVID-19%20AND%20CORONAVIRUS"]

for index in range(len(topics)):

    url_template = "https://app.leg.wa.gov/bi/report/topicalindex/"
    url = url_template + topics[index]

    result = None
    while result is None:
        try:
            s = HTMLSession()
            response = s.get(url)
            response.html.render(wait=2, sleep=3)
            soup = BeautifulSoup(response.html.html, "html.parser")
            totalData = soup.find(id="topicalIndexReportData")
            h3 = totalData.find("h3")
            first_span = h3.find("span")
            result = True
        except:
            pass

    response.close()

    main_topic = h3.find("a").text

    main_topic_underscore = main_topic.replace(" ", "_")

    with open("revised_topic_CSVs/" + main_topic_underscore + ".csv", mode='w') as file:

        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        ul = totalData.find("ul").find("ul")

        for paragraph in ul.find_all("li"):
            main_bill = [main_topic]
            text = paragraph.text
            text = " ".join(text.split())
            description = text.split(":")[0]
            main_bill.append(description)
            links = paragraph.find_all("a")
            for link in links:
                href = link.get("href")
                bill = []
                bill.extend(main_bill)
                bill.append(href)
                d = HTMLSession()
                response_d = d.get(href)
                response_d.html.render()
                soup_d = BeautifulSoup(response_d.html.html, "html.parser")
                bill_name = soup_d.find_all("div", class_="billStatusAtAGlanceSubText")[0].text
                current_status = soup_d.find_all("div", class_="billStatusAtAGlanceSubText")[1].text
                current_status = current_status.strip()
                bill.append(bill_name)
                bill.append(current_status)
                div = soup_d.find(id="horizontalStatusDisplay").find("div", class_="col-xs-12")
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
                div = soup_d.find("div", class_="container-fluid").find("div", class_="row clearfix").findChildren("div",class_=None)[5]
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
                response_d.close()
                csv_writer.writerow(bill)
