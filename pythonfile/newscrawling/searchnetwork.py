from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import MeCab, datetime
from time import sleep
from wordcloud import WordCloud
#import newscofig

date = str(datetime.date.today())
#logger = newscofig.logger
#ネットに接続するdriverを作ってreturnするメソッド
#optionsでchromeのwindowを開かずにする
def setdriver(search):
    #logger.info("set driver")
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    chrome_service = Service(executable_path="C:/Users/mg-e1/Desktop/mg/chromedriver.exe")
    driver = webdriver.Chrome(service=chrome_service, options = options)
    driver.get("https://news.yahoo.co.jp/search?p="+search+"&ei=utf-8") #住所で接続してページの情報を表示する
    
    #logger.info("return driver")
    return driver

#形態素解析をするメソッド
#driverで接続したページの中のニュース記事の住所を持ってきて記事の内容を形態素解析する
def mecabs(news, driver):
    #logger.info("start mecab")
    formecab = ""
    links = [n.get_attribute("href") for n in news]

    for link in links :
        #logger.info("now link : "+link)
        driver.execute_script('window.open("'+link+'");')
        driver.switch_to.window(driver.window_handles[1])

        try :  
            script = driver.find_element_by_xpath("/html/body/div[1]/div/main/div[1]/div/article/div[1]").text
        except Exception as e:
            #logger.warn(e)
            continue

        script = script.replace(" ", "")
        script = script.replace("\n", "")

        tempmecab = MeCab.Tagger().parse(script).splitlines()

        for line in tempmecab :
            if "名詞" in line : #名詞だけをformecabに保存する
                temp = line.split()[0]
                temp = temp.replace("'","")
                formecab = formecab +" "+ temp
        sleep(10)
    #logger.info("end mecab")
    return formecab

#wordcloudを作成するメソッド
#driverでネットに接続、mecabsで名詞だけを持って来てwordcloudにする
def wordcloudmethod(search):
    print(search)
    #logger.info("start wordcloud")
    driver = setdriver(search)
    news = driver.find_elements_by_class_name("viewableWrap newsFeed_item newsFeed_item-normal newsFeed_item-ranking ")
    words = mecabs(news, driver)
    #logger.info("draw wordcloud")
    wc = WordCloud(width=400, height=400, scale=2.0, max_font_size=250, font_path="C:/Windows/Fonts/HGRGE.TTC")
    wc.generate(words)
    wc.to_file('./static/image/word('+date+').jpg')
    #logger.info("end wordcloud")





