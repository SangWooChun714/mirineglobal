from bs4 import BeautifulSoup
from datetime import date
import drawfin, sys, csv, requests, datetime, re
from openpyxl import load_workbook
from kabuconfig import logger


kabunames = "" #검색할 회사 이름을 저장할 변수
code = "" #회사 코드를 저장할 변수
holyday_list = ["0101", "0301", "0505", "0606", "0815", "1003", "1009", "1225"] #휴일은 주식시장이 안열려 자료가 없기 때문에 휴일을 제외하기 위한 공휴일 리스트
fine_days = ["", ""]
todays = str(date.today().strftime("%Y.%m.%d")) # 오늘 날짜를 저장하는 변수
total = [] # 회사이름, 날짜, 주가, 거래량을 저장할 리스트 변수
tablenum = "" #주식차트를 가져올 때 마지막 게시판 번호를 저장하는 변수
headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}

def table_number(url) :
    try:
        res1 = requests.get(url, headers=headers) #자료값을 가져오기 위해 새로운 주소를 불러옴
        searchday = BeautifulSoup(res1.text, "lxml") #새로운 주소의 내용을 담음
        searchtablenum = searchday.find("td", attrs={"class":"pgRR"}) # 네비게이션 페이지의 끝을 확인
        if not searchtablenum:
            searchtablenum = searchday.find("table", attrs={"class":"Nnavi"}).find("td",{"class":"on"})
            tablenum = searchtablenum.a.get("href").rsplit("=")[2]
        else :
            tablenum = searchtablenum.a.get("href").rsplit("=")[2] #페이지의 끝번호만을 축출
        logger.info("url : "+url+", tablenum : "+tablenum)
    except Exception as e:
        print(e)
    return tablenum


def SearchKabuKa(kabunames, code, days):

    breaker = True # 특정 날짜가 되면 무한문을 멈출 변수
    url = "https://finance.naver.com/item/sise_day.naver?code="+code # 회사의 주가를 가져올 사이트

    logger.info("start kabusearch")
    tablenum = table_number(url)
    try:
        #with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        f = open(filename, "w", encoding="utf-8-sig", newline="") # 자료를 저장할 csv파일을 생성, 열기
        logger.info("create csv file")
        writer = csv.writer(f)
        tittle = ["종목명","종목코드", "날짜", "종합가격", "거래량"] #첫줄을 인덱스구문으로 삽입
        writer.writerow(tittle)

        for i in range(1, int(tablenum)+1): # 첫 페이지부터 ~ 끝페이지까지를 읽기위해 무한문사용
            items2 = url+"&page="+str(i) # 주소값 + 페이지 번호로 해당 페이지 접속
            res1 = requests.get(items2, headers=headers)
            searchday = BeautifulSoup(res1.text, "lxml")
            table_rows = searchday.find("table", attrs={"class":"type2"}).find_all("tr") # 자료의 값이 들어있는 테이블의 행을 모두 가져옴

            for row in table_rows:
                colums = row.find_all("td") # 행에서 각각의 열 값만을 빼내와 저장

                if len(colums) <= 1:
                    continue

                data = [column.get_text().strip() for column in colums] # 행에서 필요한 값많을 축출
                day = data[0] # 날짜를 저장
                price = data[1] # 종가를 저장
                qunt = data[6] # 거래량을 저장
                if todays == day: #오늘 날짜의 종가는 나오지 않았기에 오늘날짜를 제외시킴
                    continue
                if day == days[0] or day == days[1]: #  찾고자 하는 날짜까지 저장후 종료
                    breaker = False
                    total = [kabunames, code, day, price, qunt]
                    writer.writerow(total)
                    break

                total = [kabunames, code, day, price, qunt] # 원하는 자료만을 저장
                writer.writerow(total) # csv파일에 한 행씩 작성
                
            if breaker == True:
                continue
            else : 
                print("작업종료")
                logger.info("over csv saved")
                break

        f.close() # 작업 완료 후 csv파일을 닫고 저장

    except Exception as e:
        print(e)

    logger.info("draw graph")
    

def checking(kabunames, days):
    logger.info("start checking")
    name_compiler = any(specialtext in kabunames for specialtext in "!@#$%^&*()[]-=+_~`;'/?.<>, \t \n")
    print(name_compiler)

    if name_compiler == True :
        logger.warning("companyname error. input kabu : "+kabunames)
        print("주식이름 이상, 입력받은 주식이름 : "+kabunames)
        sys.exit()
    
    date_compiler = re.compile(r"([12]\d{3}).(0\d|1[0-2]).([0-2]\d|3[01])$")
    date_check = date_compiler.match(days)
    print(date_check)
    if not date_check:
        logger.warning("date error. input dayte : "+days)
        print("날짜를 정확히 입력해주세요. 입력받은 날짜 : "+days)
        sys.exit()
    logger.info("end checking")


def FindDays(days) :
    logger.info("start finddays")
    list_date = days.split(".")
    years = int(list_date[0])
    months = int(list_date[1])
    days = int(list_date[2])

    str_monday = list_date[1]+list_date[2] # 지정된 날짜가 휴일인지 확인을 위해 저장하는 변수
    weekendday = datetime.date(years, months, days).weekday()
    temp_date = datetime.date(years, months, days)

    if weekendday >= 5 or str_monday in holyday_list: # 공휴일이거나 주말이라면 바로 앞의 날짜가 나오도록 하는 함수 ex) 공휴일이 금요일일 경우 목요일 출력, 주말일 경우 금요일 출력
        temp_date1 = str(temp_date - datetime.timedelta(max(1, (weekendday+6)%7-3))).split("-")
        temp_date2 = str(temp_date - datetime.timedelta(max(2, (weekendday+6)%7-2))).split("-")
        fine_days[0] = temp_date1[0]+"."+temp_date1[1]+"."+temp_date1[2]
        fine_days[1] = temp_date2[0]+"."+temp_date2[1]+"."+temp_date2[2]
    else : 
        temp_date = str(temp_date).split("-")
        fine_days[0] = (temp_date[0]+"."+temp_date[1]+"."+temp_date[2]) #마지막 결과값 저장
    logger.info("end finddays")
    return fine_days


if __name__ == "__main__":
    args = sys.argv
    kabunames = args[1] #입력 받은 파라미터값은 리스트로 들어옴, 리스트의 두번째가 회사 이름
    inputdays = args[2] # 세번째 인자는 날짜 2022.02.07로 들어오기에 각각의 숫자를 나눔

    checking(kabunames, inputdays)

    filename = kabunames + ".csv" # csv파일 이름

    search_date = FindDays(inputdays)
    
    wb = load_workbook("상장법인목록.xlsx") #회사코드를 알기 위해 엑셀파일을 불러옴
    ws = wb.active
    for row in ws.iter_rows(min_row=2): #엑셀파일에서 회사코드 확인 후 자료찾기 함수에 값을 넣어줌
        if row[0].value == kabunames:
            code = row[1].value
            wb.close()
            SearchKabuKa(kabunames, code, search_date)
            break
    
    drawfin.drawline(filename) # 자료를 활용하여 그래프 그리기 함수


