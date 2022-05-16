from io import StringIO
from mongoconfig import logger
import requests, datetime
from bs4 import BeautifulSoup
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from urllib.request import urlopen
from pymongo import MongoClient



def geturls():

    today = str(datetime.date.today().strftime("%Y%m%d"))
    #url = "https://www.release.tdnet.info/inbs/I_list_001_20220516.html"
    url = "https://www.release.tdnet.info/inbs/I_list_001_"+today+".html"
    headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}#heaaderを指定
#headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}#heaaderを指定
    requst = requests.get(url=url, headers=headers)
    searchurl = BeautifulSoup(requst.text, "lxml")
    tempurl = searchurl.find_all("td", attrs={"class" : "oddnew-M kjTitle"})

    urls = []
    for j in tempurl:
        urls.append("https://www.release.tdnet.info/inbs/"+j.find("a").get("href"))
    
    return urls

def compilefiles(links):

    content = []

    for link in links:

        file = urlopen(link)
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()

        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        device.close()

        process_pdf(rsrcmgr, device, file)
        temp = retstr.getvalue()

        temp = temp.replace(" ", "")
        temp = temp.replace("\n", "")
        content.append(temp)
        retstr.close()

    return content

def savedb():
    logger.info()
    clients = MongoClient("mongodb://root:example@localhost:27017/")
    db = clients.mongo_crontab

if __name__ == "__main__":
    logger.info("start mongo crawling")
    links = geturls()
    compilefiles(links)
    savedb()
    logger.info("end mongo crawling")


