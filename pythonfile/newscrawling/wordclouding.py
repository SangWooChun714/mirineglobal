from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import MeCab
from time import sleep
from wordcloud import WordCloud
import matplotlib.pyplot as plt


#ネットに接続するdriverを作ってreturnするメソッド
#optionsでchromeのwindowを開かずにする
def setdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    chrome_service = Service(executable_path="C:/Users/mg-e1/Desktop/mg/chromedriver.exe", options=options)
    driver = webdriver.Chrome(service=chrome_service)
    driver.get("https://news.yahoo.co.jp/categories/domestic") #住所で接続してページの情報を表示する
    return driver

#形態素分析をするメソッド
#driverで接続したページの中のニュース記事の住所を持ってきて記事の内容を形態素解析する
def mecabs(politic, driver):
    n = 0
    formecab = ""
    links = [n.get_attribute("href") for n in politic]

    for link in links :
        print(link)
        driver.execute_script('window.open("'+link+'");')
        driver.switch_to.window(driver.window_handles[1])

        try :  
            script = driver.find_element_by_xpath("/html/body/div[1]/div/main/div[1]/div/article/div[1]/div/p").text
        except Exception as e:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
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

    return formecab

#wordcloudを作成するメソッド
#driverでネットに接続、mecabsで名詞だけを持って来てwordcloudにする
def wordcloud():
    driver = setdriver()
    politic = driver.find_elements_by_class_name("newsFeed_item_link")
    words = mecabs(politic, driver)
    print(words)
    wc = WordCloud(width=400, height=400, scale=2.0, max_font_size=250, font_path="C:/Windows/Fonts/HGRGE.TTC")
    gen = wc.generate(words)
    wc.to_file('word.jpg')

if(__name__ == "__main__"):
    script = wordcloud()
