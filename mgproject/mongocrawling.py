from io import StringIO
from mongoconfig import logger
import requests, datetime
from bs4 import BeautifulSoup
from pdfminer.pdfinterp import PDFResourceManager, PDFPage, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import BytesIO
from urllib.request import urlopen
from pymongo import MongoClient


def gettablenum(today):
    
    #tempurl = "https://www.release.tdnet.info/inbs/I_list_001_20220516.html"
    url = "https://www.release.tdnet.info/inbs/I_list_001_"+today+".html"
    headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}#heaaderを指定
#headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}#heaaderを指定
    requst = requests.get(url=url, headers=headers)
    searchurl = BeautifulSoup(requst.text, "lxml")
    tablenum = searchurl.find_all("div", attrs={"class" : "pager-M"})
#print(tablenum[-1].get_text())
    tablenum = int(tablenum[-1].get_text())
    return tablenum

def geturls():

    today = str(datetime.date.today().strftime("%Y%m%d"))

    tablenum = gettablenum(today)

    for i in range(0, tablenum):
    #url = "https://www.release.tdnet.info/inbs/I_list_001_20220516.html"
        url = "https://www.release.tdnet.info/inbs/I_list_00"+str(i)+"_"+today+".html"
        headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}#heaaderを指定
#headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}#heaaderを指定
        requst = requests.get(url=url, headers=headers)
        searchurl = BeautifulSoup(requst.text, "lxml")
        tempurl = searchurl.find_all("td", attrs={"class" : "oddnew-M kjTitle"})

        urls = []
        for j in tempurl:
            urls.append("https://www.release.tdnet.info/inbs/"+j.find("a").get("href"))
    
    return urls

def readpdfs(links):

    content = []

    for link in links:

        tempfiles = urlopen(link).read()
        files = BytesIO(tempfiles)

        retstr = StringIO()
        parser = PDFParser(files)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, retstr, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

        temp = retstr.getvalue()

        temp = temp.replace(" ", "")
        temp = temp.replace("\n", "")
        content.append(temp)
        retstr.close()

    return content

def savedb(content):
    logger.info()
    clients = MongoClient("mongodb://root:example@localhost:27017/")
    db = clients.mongo_crontab
    

if __name__ == "__main__":
    logger.info("start mongo crawling")
    links = geturls()
    content = readpdfs(links)
    savedb(content)
    logger.info("end mongo crawling")


