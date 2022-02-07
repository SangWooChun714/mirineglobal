from ast import arg
from msilib.schema import Error
from tkinter import E
from bs4 import BeautifulSoup
from datetime import date
import drawfin, sys, csv, requests, datetime
from openpyxl import load_workbook

kabunames = ""
code = 0
holyday_list = ["0101", "0301", "0505", "0606", "0815", "1003", "1009", "1225"]

def searchkabuka(kabunames, code, days):
 
    total = []
    breaker = True
    jongmok = kabunames+"("+code+")"
    filename = "주식이력.csv"
    tablenum = ""

    datetims = date.today()
    datetims = str(datetims.strftime("%Y.%m.%d"))
    
    url = "https://finance.naver.com/item/sise.naver?code="+code
    url2 = "https://finance.naver.com"

    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        items1 = soup.find("iframe", attrs={"title":"일별 시세"})["src"]
        items1 = url2+items1
        print(items1)
        headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
        res1 = requests.get(items1, headers=headers)
        searchday = BeautifulSoup(res1.text, "lxml")
        searchtablenum = searchday.find("table", attrs={"class":"Nnavi"}).find("td", class_="pgRR")
        tablenum = searchtablenum.a.get("href").rsplit("&")[1].split("=")[1]
    except Exception as e:
        print(e)

    try:
        f = open(filename, "w", encoding="utf-8-sig", newline="")
        writer = csv.writer(f)
        tittle = ["종목명", "날짜", "종합가격", "거래량"]
        writer.writerow(tittle)

        for i in range(1, int(tablenum)+1):
            items2 = items1+"&page="+str(i)
            print(items2)
            headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
            res1 = requests.get(items2, headers=headers)
            searchday = BeautifulSoup(res1.text, "lxml")
            table_rows = searchday.find("table", attrs={"class":"type2"}).find_all("tr")

            for row in table_rows:
                colums = row.find_all("td")

                if len(colums) <= 1:
                    continue

                data = [column.get_text().strip() for column in colums]
                day = data[0]
                price = data[1]
                qunt = data[6]

                if datetims == day:
                    continue
                if day == days:
                    breaker = False
                    total = [jongmok, day, price, qunt]
                    writer.writerow(total)
                    break

                total = [jongmok, day, price, qunt]
                writer.writerow(total)

            if breaker == True:
                continue
            else : 
                print("작업종료")
                break

        f.close()

    except Exception as e:
        print(e)

    drawfin.drawline(filename)

if __name__ == "__main__":
    args = sys.argv 
    kabunames = args[1]
    inputdays = args[2].split(".")
    if len(kabunames) <= 0 or len(kabunames) >= 15 or any(x in kabunames for x in "!@#$%^&*()[];,./'") == True:
        print("정확한 회사명을 입력해 주세요.")
        raise Error
    elif len(inputdays[0]) >= 5 or len(inputdays[0]) <= 0 or len(inputdays[1]) >= 2 or len(inputdays[1]) <= 0 or len(inputdays[2]) >= 2 or len(inputdays[2]) <=0:
        print("날짜를 정확하게 입력해 주세요")
        raise Error
    else :
        try:
            years = int(inputdays[0])
            months = int(inputdays[1])
            days = int(inputdays[2])
        except Exception as e:
            print("날짜를 정확하게 입력해 주세요")
        strmonday = inputdays[1]+inputdays[2]
        weekendday = datetime.date(years, months, days).weekday()
        temp_date = datetime.date(years, months, days)

        if weekendday >= 5 or strmonday in holyday_list:
            temp_date = temp_date - datetime.timedelta(max(1, (weekendday+6)%7-3))
        else : 
            temp_date = str(temp_date).split("-")
        finedays = temp_date[0]+"."+temp_date[1]+"."+temp_date[2]
    
        wb = load_workbook("상장법인목록.xlsx")
        ws = wb.active
        for row in ws.iter_rows(min_row=2):
            if row[0].value == kabunames:
                code = row[1].value
                wb.close()
                searchkabuka(kabunames, code, finedays)
                break
    



