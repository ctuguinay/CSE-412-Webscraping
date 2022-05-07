from bs4 import BeautifulSoup
from requests_html import HTMLSession
import csv

url = "https://leg.wa.gov/house/representatives/Pages/default.aspx"

result = None
while result is None:
    try:
        s = HTMLSession()
        response = s.get(url)
        response.html.render(wait=2, sleep=3)
        soup = BeautifulSoup(response.html.html, "html.parser")
        members = soup.find_all("span", class_="memberName")
        result = True
    except:
        pass

with open("representatives.csv", mode='w') as file:

    csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    for member in members:
        text = member.text
        name = text.replace("Representative ", "").replace(" (R)", "").replace(" (D)", "")
        party = text[len(text) - 3:].replace("(", "").replace(")", "")
        data = [name, party]
        csv_writer.writerow(data)

url = "https://leg.wa.gov/Senate/Senators/Pages/default.aspx"

result = None
while result is None:
    try:
        s = HTMLSession()
        response = s.get(url)
        response.html.render(wait=2, sleep=3)
        soup = BeautifulSoup(response.html.html, "html.parser")
        members = soup.find_all("span", class_="memberName")
        result = True
    except:
        pass

with open("senators.csv", mode='w') as file:

    csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    for member in members:
        text = member.text
        name = text.replace("Senator ", "").replace(" (R)", "").replace(" (D)", "")
        party = text[len(text) - 3:].replace("(", "").replace(")", "")
        data = [name, party]
        csv_writer.writerow(data)