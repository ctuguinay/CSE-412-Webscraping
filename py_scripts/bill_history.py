from bs4 import BeautifulSoup
from requests_html import HTMLSession
import csv
import datetime


def month_to_number(month):
    datetime_object = datetime.datetime.strptime(month, "%b")
    month_number = int(datetime_object.month)
    return month_number


with HTMLSession() as session:
    with open("bill_history_CSVs/bill_history_revised.csv", mode='w', newline='') as file:

        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        url = "https://app.leg.wa.gov/billsummary?BillNumber=1162&Year=2021&Initiative=false"

        response = session.get(url)
        response.html.render()
        soup = BeautifulSoup(response.html.html, "html.parser")

        clearfix_rows = soup.find(id="pageContent").find_all("div", class_="row clearfix")
        count = 0
        for row in clearfix_rows:
            if "Bill Not Found." in row.text:
                count = count + 1
        if not count > 0:
            div = soup.find("div", class_="container-fluid").find("div", class_="row clearfix").findChildren("div",
                                                                                               class_=None)[5]
            divs = div.find_all("div", class_="row clearfix")
            bill_history = soup.find("div", class_="col-xs-12 col-csm-11 col-sm-10 col-md-9 col-lg-10")
            p_list = bill_history.find_all("p")
            history_table_list = bill_history.find_all("div", class_="historytable")
            string = ""
            header = ["Session", "Date", "Action", "Days Since First", "Days Till Today", "Days At Action",
                      "Simplified Action"]
            csv_writer.writerow(header)
            cur_year = "2021"
            first_date = None
            bill = []
            for index in range(len(p_list)):
                total = []
                p = p_list[index]
                step = p.text.strip()
                if "2022" in step:
                    cur_year = "2022"
                history_table = history_table_list[index]
                dates = history_table.find_all("div", class_="historyrow")
                texts = history_table.find_all("div", attrs={'style': 'display: table-cell; padding-right: 0.5em;'})
                count = 0
                for i in range(len(texts)):
                    text = texts[i].text.split("(")[0].strip()
                    date = dates[i].text.strip()
                    combine = [date, text]
                    total.append(combine)
                revised_total = []
                for i in range(len(total)):
                    cur_date = total[i][0]
                    cur_text = total[i][1]
                    if len(cur_date) == 0:
                        revised_total[len(revised_total) - 1][1] = revised_total[len(revised_total) - 1][
                                                                       1] + " " + cur_text
                    else:
                        revised_total.append(total[i])
                for i in range(len(revised_total)):
                    date = revised_total[i][0]
                    text = revised_total[i][1]
                    revised_total[i][1] = " ".join(text.split())
                    if "Dec" in date:
                        if cur_year == "2021":
                            date = date + " 2020"
                        else:
                            date = date + " 2021"
                    else:
                        date = date + " " + cur_year
                    revised_total[i][0] = date
                f_date_split = revised_total[0][0].split()
                if not first_date:
                    first_date = datetime.datetime(int(f_date_split[2]), month_to_number(f_date_split[0]),
                                                   int(f_date_split[1]))
                total_days_array = []
                for i in range(len(revised_total)):
                    date_split = revised_total[i][0].split()
                    date = datetime.datetime(int(date_split[2]), month_to_number(date_split[0]),
                                             int(date_split[1]))
                    difference = date - first_date
                    total_days_spent = difference.days
                    total_days_array.append(total_days_spent)
                for i in range(len(revised_total)):
                    date_split = revised_total[i][0].split()
                    date = datetime.datetime(int(date_split[2]), month_to_number(date_split[0]),
                                             int(date_split[1]))
                    now_date = datetime.datetime.now()
                    difference = now_date - date
                    days_between_now = difference.days
                    bill.append([step] + revised_total[i] + [total_days_array[i]] + [days_between_now])
            for i in range(len(bill)):
                sub_bill = bill[i]
                if i == len(bill) - 1:
                    sub_bill.append(sub_bill[4])
                else:
                    next_sub_bill = bill[i+1]
                    sub_bill.append(next_sub_bill[3] - sub_bill[3])
                csv_writer.writerow(sub_bill)
            response.close()
