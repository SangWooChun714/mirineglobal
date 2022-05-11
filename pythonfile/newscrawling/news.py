from selenium import webdriver
from datetime import date
import ssl
from elasticsearch import Elasticsearch
from newscofig import logger
from selenium.webdriver.chrome.service import Service




#elasticに保存する関数
#ctxほelasticsearchの認証書
#indexはelasticsearchに保存するindex名
#todaysは今日を保存する
def elastic(newspage, n, driver):
    logger.info("start elastic")

    todays = str(date.today().strftime("%Y.%m.%d")) # 今日の日付を保存
    ctx = ssl.create_default_context()
    ctx.load_verify_locations("C:/Users/mg-e1/Desktop/elasticsearch-8.1.0/cert1/http_ca.crt")
    es = Elasticsearch("https://localhost:9200", basic_auth=("elastic","sw1594311") ,ssl_context=ctx)
    index = "dailynews"

    tempdate = todays.split(".")
    iddate = tempdate[0]+tempdate[1]+tempdate[2]
    
    for i in newspage:

        iddate1 = iddate+"("+str(n)+")"

        link = i.get_attribute("href")
        driver.execute_script('window.open("'+link+'");')
        driver.switch_to.window(driver.window_handles[1])

        script1 = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[1]/div[1]/div[2]/div[1]").text
        script1 = script1.replace(" ", "")
        script1 = script1.replace("\n", "")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        body = {
            "date" : todays,
            "title" : i.text,
            "link" : link,
            "script" : script1
        }
        
        es.index(index = index, id=iddate1, document = body)
        n += 1
    logger.info("end elastic")
    return n

#ウェブからニュースをcrawlingしてealsticsearchに保存する関数

def newscraling():
    logger.info("newsstart")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    n = 1
    chrome_service = Service(executable_path="C:/Users/mg-e1/Desktop/mg/chromedriver.exe")
    driver1 = webdriver.Chrome(service=chrome_service, options=options)
    #driver2 = webdriver.Chrome("C:/Users/cjstk/Desktop/mirineglobal/chromedriver.exe", options=options)

    logger.info("pol news start")
    driver1.get("https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100")
    politicsnews = driver1.find_elements_by_class_name("cluster_text_headline")
    n = elastic(politicsnews, n, driver1)
    logger.info("pol news end, n = "+str(n))

    logger.info("eco news start")
    driver1.get(driver1.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div/div/div[1]/div/ul/li[3]/a").get_attribute("href"))
    econews = driver1.find_elements_by_class_name("cluster_text_headline")
    n = elastic(econews, n, driver1)
    logger.info("eco news end, n = "+str(n))



if __name__ == "__main__" :
    logger.info("start news work")
    newscraling()
    logger.info("end news work")
