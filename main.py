from bs4 import BeautifulSoup
from requests_html import HTMLSession

url = "https://app.leg.wa.gov/bi/report/topicalindex/?biennium=2021-22&topicId=14720"

s = HTMLSession()
response = s.get(url)
response.html.render(wait=2, sleep=3)

soup = BeautifulSoup(response.html.html, "html.parser")

totalData = soup.find(id = "topicalIndexReportData")

h3 = totalData.find("h3")

first_span = h3.find("span")

links = []

for link in first_span.find_all('a'):
    href = link.get('href')
    href = href.replace(" ", "%20")
    links.append(href)

ul = totalData.find("ul")

print(ul)