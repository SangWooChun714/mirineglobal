from ast import arg
from bs4 import BeautifulSoup
from datetime import date
import drawfin, sys, csv, requests
from openpyxl import load_workbook

kabunames = ""
code = 0
def searchkabuka(code, days):
    print(type(days))
    
    total = []
    breaker = True

    datetims = date.today()
    datetims = str(datetims.strftime("%Y.%m.%d"))

    filename = "주식이력.csv"
    f = open(filename, "w", encoding="utf-8-sig", newline="")
    writer = csv.writer(f)
    tittle = ["종목명", "날짜", "종합가격", "거래량"]
    writer.writerow(tittle)
    
    url = "https://finance.naver.com/item/sise.naver?code="+code
    url2 = "https://finance.naver.com"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")

    kabu = soup.find("div", attrs={"class":"h_company"}).find("a").get_text()
    jongmok = kabu+"("+code+")"

    items1 = soup.find("iframe", attrs={"title":"일별 시세"})
    items2 = url2+items1['src']

    headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
    res1 = requests.get(items2, headers=headers)
    searchday = BeautifulSoup(res1.text, "lxml")
    searchtablenum = searchday.find("table", attrs={"class":"Nnavi"})
    tablenum = searchtablenum.find("td", class_="pgRR")
    tablenum = tablenum.a.get("href").rsplit("&")[1]
    tablenum = tablenum.split("=")[1]

    for i in range(1, int(tablenum)):
        items2 = url2+items1['src']+"&page="+str(i)
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
            print(day,"day",type(day))
            print(days,"days")
            if day == days:
                print("들어옴")
                breaker = False
                break

            total = [jongmok, day, price, qunt]
            writer.writerow(total)

        print()
        if i == 2:
            break

        if breaker == True:
            continue
        else : 
            print("작업종료")
            break

    f.close()
    drawfin.drawline(filename)

if __name__ == "__main__":
    args = sys.argv
    print(args)
    if args[1] == int :
        print("검색하는 회사의 이름을 정확하게 입력해주세요.")
    else:
        kabunames = args[1]
        days = args[2]
        wb = load_workbook("상장법인목록.xlsx")
        ws = wb.active
        for row in ws.iter_rows(min_row=2):
            if row[0].value == kabunames:
                code = row[1].value
                wb.close()
        print(code)
        searchkabuka(code, days)



