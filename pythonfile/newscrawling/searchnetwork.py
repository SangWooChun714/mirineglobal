import MeCab, datetime, requests, logging
from wordcloud import WordCloud
from bs4 import BeautifulSoup



logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s- %(funcName)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("websearchnews.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

date = str(datetime.date.today())

def searchnetwork(search):

    logger.info("start searchnetwork")
    if search =="search is empty":
        url = "https://news.yahoo.co.jp/"
    else : 
        url = "https://news.yahoo.co.jp/search?p="+search+"&ei=utf-8" 
    words = ""
    __headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}#heaaderを指定
    res1 = requests.get(url=url, headers=__headers)
    searchday = BeautifulSoup(res1.text, "lxml")
    divnews = searchday.find_all("div", attrs={"class":"newsFeed_item_text"})# tableから資料を持ってくる
    for i , j in enumerate(divnews):
        newstitle = j.find("div", attrs={"class":"newsFeed_item_title"}) # tableから資料を持ってくる
        newsbody = j.find("div", attrs={"class":"sc-cnyaSH kPLsVs"})
        words = words + newstitle.text + newsbody.text
    words = words.replace(" ", "")
    words = words.replace("\n", "")
    logger.info("end searchnetwork")
    return words

def wordcloudmethod(search):

    logger.info("start wordcloud")
    words = searchnetwork(search)
    tempmecab = MeCab.Tagger().parse(words).splitlines()
    mecabs = ""
    for line in tempmecab :
        if "名詞" in line : #名詞だけをformecabに保存する
            temp = line.split()[0]
            temp = temp.replace("'","")
            mecabs = mecabs +" "+ temp
    
    wc = WordCloud(width=400, height=400, scale=2.0, max_font_size=250, font_path="C:/Windows/Fonts/HGRGE.TTC")
    ad =wc.generate(mecabs)
    wc.to_file('./static/image/'+search+'word('+date+').jpg')
    filenames = search+'word('+date+').jpg'
    logger.info("end wordcloud")
    return filenames