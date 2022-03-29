from selenium import webdriver
from time import sleep
from datetime import date
import ssl
from elasticsearch import Elasticsearch
from newscofig import logger


def newscraling():

    todays = str(date.today().strftime("%Y.%m.%d")) # 今日の日付を保存
    
    ctx = ssl.create_default_context()
    ctx.load_verify_locations("C:/Users/cjstk/Desktop/elasticsearch-8.1.0/cert1/http_ca.crt")
    es = Elasticsearch("https://localhost:9200", basic_auth=("elastic","sw1594311") ,ssl_context=ctx)
    index = "dailynews"

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver1 = webdriver.Chrome("C:/Users/cjstk/Desktop/mirineglobal/chromedriver.exe", options=options)

    driver1.get("https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100")
    newslink = driver1.find_elements_by_class_name("cluster_text_headline")
    n = 1
    tempdate = todays.split(".")
    iddate = tempdate[0]+tempdate[1]+tempdate[2]

    for i in newslink:
        iddate1 = iddate+"("+str(n)+")"
        body = {
            "date" : todays,
            "title" : i.text,
            "link" : i.get_attribute("href"),
        }
        es.index(index = index, id=iddate1, document = body)
        n += 1

if __name__ == "__main__" :
    logger.info("start news work")
    newscraling()
    logger.info("end news work")
