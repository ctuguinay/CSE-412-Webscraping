from bs4 import BeautifulSoup
from requests_html import HTMLSession
import csv

url = "https://leg.wa.gov/house/representatives/Pages/default.aspx"

result = None
while result is None:
    try:
        s = HTMLSession()
        response = s.get(url)

        result = True
    except:
        pass