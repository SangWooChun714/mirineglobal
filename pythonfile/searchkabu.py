from openpyxl import load_workbook
from bs4 import BeautifulSoup
import requests

wb = load_workbook("상장법인목록.xlsx") # 상장된 회사 목록과 회사 코드가 저장된 파일을 불러옴(출처 : https://kind.krx.co.kr/main.do?method=loadInitPage&scrnmode=1)
ws = wb.active #파일 내부의 sheet 활성화

def searchkabu(kabu):

    code = 0 # 회사코드를 저장할 변수
    upper = "" # 전날대비 상승인지 하락인지를 확인하고 저장할 변수
    differ = "" # 전날대비 차액을 저장할 변수
    quant = "" # 거래량을 저장할 변수
    nowval = "" # 현재가격을 저장할 변수

    for row in ws.iter_rows(min_row=2): # 서버에서 검색할 회사 이름을 받아와 파일에서 검색하여 코드를 찾아오는 함수
        if row[0].value == kabu:
           code = row[1].value
           wb.close()
        
    url = "https://finance.naver.com/item/sise.naver?code="+code # 주식의 가격을 확인하기 위해 사이트에 접속, 접속 시 회사코드를 활용하여 특정회사를 검색
    res = requests.get(url)
    jongmok = BeautifulSoup(res.text, "lxml")

    searchnowval = jongmok.find("strong", attrs={"id":"_nowVal"}) # 페이지를 검색하여 현재가격을 찾아서 저장
    nowval = searchnowval.get_text() # html 태그가 모두 포함되어 들어오기때문에 get_text()로 값만을 가져옴

    diff = jongmok.find_all("strong", attrs={"id":"_diff"}) # 전날대비 차액을 가져오는 코드
    for i in diff:
      sub = i.get_text()
      sub = sub.split() # 하락, 상승, 차액, 화살표 그림이 들어가도록 코드가 짜여있어 띄어쓰기가 나오므로 빈공간을 잡아서 문자열로 반환
      upper = sub[0]
      differ = sub[1]

    searchquant = jongmok.find("span", attrs={"id":"_quant"}) # 거래량을 가져오는 코드
    quant = searchquant.get_text()
    return code, nowval, quant, upper, differ # 모든 정보를 리턴





