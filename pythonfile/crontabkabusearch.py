from time import sleep
from bs4 import BeautifulSoup
from datetime import date
import requests, ssl
from elasticsearch import Elasticsearch
import logging
import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s- %(funcName)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("dailykabulog.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#株価をcrawlingする関数
#totalで架空した資料を保存
#tablenumで持ってくるpageを決定
#dayは今処理しているひ、daysは入力された日
def SearchKabuKa():
    logger.info("start kabusearch")
    __headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}#heaaderを指定
    todays = str(date.today().strftime("%Y.%m.%d")) # 今日の日付を保存
    kabunames = "삼성전자"
    code = "005930"
    url = "https://finance.naver.com/item/sise_day.naver?code="+code # 株価を持ってくる住所
    ctx = ssl.create_default_context()
    ctx.load_verify_locations("C:/Users/cjstk/Desktop/elasticsearch-8.1.0/cert1/http_ca.crt")
    es = Elasticsearch("https://localhost:9200", basic_auth=("elastic","sw1594311") ,ssl_context=ctx)
    index = "dailykabu"
    n = int(todays.split(".")[-1])
    logger.info("id = "+str(n))
    try:
        res1 = requests.get(url, headers=__headers)
        searchday = BeautifulSoup(res1.text, "lxml")
        table_rows = searchday.find("table", attrs={"class":"type2"}).find_all("tr") # tableから資料を持ってくる
        for row in table_rows:
            colums = row.find_all("td")
            if len(colums) <= 1:
                continue
            data = [column.get_text().strip() for column in colums] # 必要の数値を持ってくる
            day = data[0] # 日付
            price = data[1] # 株価
            qunt = data[6] # 取引量
            if todays == day: #　今日の資料を除く
                body = {
                    "kabuNm" : kabunames,
                    "code" : code,
                    "date" : day,
                    "kabuka" : price,
                    "volume" : qunt
                }
                es.index(index = index, id = n, document = body)
                print("작업종료")
                logger.info("end kabusearch")
                break

    except Exception as e:
        print(e)
        logger.warning(e)

if __name__ == "__main__" :
    logger.info("start work")
    os.system("wsl -d docker-desktop sysctl -w vm.max_map_count=262144")
    os.system("docker start es01")
    sleep(50)
    SearchKabuKa()#crawling関数
    os.system("docker stop es01")
    os.system("wsl -d docker-desktop sysctl -w vm.max_map_count=62144")
    logger.info("end work")

