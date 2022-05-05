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
    for link in paragraph.find_all("a"):
        href = link.get("href")
        bill.append(href)
    bills.append(bill)

print(bills)