from bs4 import BeautifulSoup
from requests_html import HTMLSession

totalData = None
h3 = None
first_span = None

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

main_topic = h3.find("a").text

links = []

for link in first_span.find_all("a"):
    href = link.get("href")
    href = href.replace(" ", "%20")
    links.append(href)

ul = totalData.find("ul").find("ul")

bills = []

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
    divs = div.find_all("div", class_="row clearfix")[2:4]
    print(divs[0].prettify())
    print(divs[1].prettify())
    response_d.close()
    bills.append(bill)