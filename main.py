from bs4 import BeautifulSoup
from requests_html import HTMLSession
import csv

totalData = None
h3 = None
first_span = None

topics = ["?biennium=2021-22&topicId=14720",
    "?biennium=2021-22&topic=BUDGETS",
    "?biennium=2021-22&topic=COMPUTERS",
    "?biennium=2021-22&topic=EMERGENCY%20MANAGEMENT%20AND%20SERVICES",
    "?biennium=2021-22&topic=EMERGENCY,%20STATE%20OF",
    "?biennium=2021-22&topic=EMPLOYMENT%20AND%20EMPLOYEES",
    "?biennium=2021-22&topic=FOOD%20AND%20FOOD%20PRODUCTS",
    "?biennium=2021-22&topic=HEALTH%20AND%20SAFETY,%20PUBLIC",
    "?biennium=2021-22&topic=HOMELESS%20PERSONS",
    "?biennium=2021-22&topic=HOMES%20AND%20HOUSING",
    "?biennium=2021-22&topic=LABOR",
    "?biennium=2021-22&topic=LONG-TERM%20CARE",
    "?biennium=2021-22&topic=MENTAL%20HEALTH",
    "?biennium=2021-22&topic=PUBLIC%20ASSISTANCE",
    "?biennium=2021-22&topic=REAL%20ESTATE%20AND%20REAL%20PROPERTY",
    "?biennium=2021-22&topic=TAX%20PREFERENCES%20-%20EXEMPTIONS,%20CREDITS,%20DEDUCTIONS,%20DEFERRALS,%20ETC.",
    "?biennium=2021-22&topic=TAXES%20-%20PROPERTY",
    "?biennium=2021-22&topic=TELECOMMUNICATIONS",
    "?biennium=2021-22&topic=UNEMPLOYMENT%20COMPENSATION",
    "?biennium=2021-22&topic=WORKERS%27%20COMPENSATION"]

url_template = "https://app.leg.wa.gov/bi/report/topicalindex/"

url = "https://app.leg.wa.gov/bi/report/topicalindex/?biennium=2021-22&topicId=14720"
result = None
while result is None:
    try:
        s = HTMLSession()
        response = s.get(url)
        response.html.render(wait=2, sleep=3)
        soup = BeautifulSoup(response.html.html, "html.parser")
        totalData = soup.find(id = "topicalIndexReportData")
        h3 = totalData.find("h3")
        first_span = h3.find("span")
        result = True
    except:
         pass

#links = []

#for link in first_span.find_all("a"):
#   href = link.get("href")
#   href = href.replace(" ", "%20")
#   print(href)
#   links.append(href)

main_topic = h3.find("a").text

main_topic_underscore = main_topic.replace(" ", "_")

with open(main_topic_underscore + ".csv", mode='w') as employee_file:

    csv_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    ul = totalData.find("ul").find("ul")

    for paragraph in ul.find_all("li"):
        bill = []
        bill.append(main_topic)
        text = paragraph.text
        text = " ".join(text.split())
        description = text.split(":")[0]
        bill.append(description)
        link = paragraph.find_all("a")[-1]
        href = link.get("href")
        bill.append(href)
        d = HTMLSession()
        response_d = d.get(href)
        response_d.html.render()
        soup_d = BeautifulSoup(response_d.html.html, "html.parser")
        bill_name = soup_d.find_all("div", class_="billStatusAtAGlanceSubText")[0].text
        current_status = soup_d.find_all("div", class_="billStatusAtAGlanceSubText")[1].text
        current_status = current_status[1:]
        current_status = current_status.strip()
        bill.append(bill_name)
        bill.append(current_status)
        div = soup_d.find(id = "horizontalStatusDisplay").find("div", class_="col-xs-12")
        svgs = div.find_all("svg")[1:4]
        for svg in svgs:
            circles = []
            circle_set = svg.find_all("circle")
            for index in range(len(circle_set)):
                circle = circle_set[index]
                if circle["fill"] == "white":
                    circles.append("0")
                elif circle["fill"] == "black":
                    circles.append("1")
            if len(circles) == 1:
                circles = ["1", "1", "1", "1"]
            bill.append(circles)
        div = soup_d.find("div", class_="container-fluid").find("div", class_="row clearfix").findChildren("div", class_=None)[5]
        divs = div.find_all("div", class_="row clearfix")
        bill.append(divs[1].text.strip())
        bill.append((" ".join(divs[2].text.split()).replace("Sponsors: ", "")))
        try:
            if "Companion Bill:" in divs[3].text.strip():
                bill.append("No Requester")
            else:
                bill.append(divs[3].text.strip().replace("\n", " ").replace("By Request: ", ""))
        except:
            bill.append("No Requester")
        # Wilson, C. and Johnson, J.
        response_d.close()
        print(bill)
        csv_writer.writerow(bill)