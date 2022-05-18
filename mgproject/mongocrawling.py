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



#TDnetのサイトで指定した日付のtableの数を得る。
#午前に作動したらtableが一つだけなので強制的に2にして1回でcrawlingが終了するようにします。
def gettablenum(today):
    logger.info("start gettablenum")

    url = "https://www.release.tdnet.info/inbs/I_list_001_"+today+".html"
    headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}#heaaderを指定
    requst = requests.get(url=url, headers=headers)
    searchurl = BeautifulSoup(requst.text, "lxml")
    tablenum = searchurl.find_all("div", attrs={"class" : "pager-M"})

    if not tablenum : 
        tablenum = 2
    else : 
        tablenum = int(tablenum[-1].get_text())

    logger.info("end gettablenum")
    return tablenum

#TDnetから情報を持ってくる関数。
#tableのtdのclass名が二つなのでifで分けます。
#urlのiのところがtable番号なのでforで変えながらcrawlingします。
#結果は辞書の形({会社のcode, 会社の名前, date, 文書のtitle, 注所,　内容})で配列に入れて返す。
def geturls():
    logger.info("start geturl")

    today = str(datetime.date.today().strftime("%Y%m%d"))
    result = []
    tablenum = gettablenum(today)

    for i in range(1, tablenum):

        url = "https://www.release.tdnet.info/inbs/I_list_00"+str(i)+"_"+today+".html"
        headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}#heaaderを指定
        requst = requests.get(url=url, headers=headers)
        requst.encoding = "utf-8"
        searchurl = BeautifulSoup(requst.text, "lxml")
        tempurl1 = searchurl.find("table", attrs={"id" : "main-list-table"})
        tempurl = tempurl1.find_all("tr")

        for j in tempurl :
            #tdのclass名がoddnew, evennewで分けて入れられているのでif文で選別する。
            if not j.find(attrs = "oddnew-M kjCode") :
                result.append({"codes" : j.find(attrs = "evennew-M kjCode").get_text(), "names" : j.find(attrs = "evennew-M kjName").get_text().replace(" ", ""), 
                "date" : today, "titles" : j.find(attrs = "evennew-M kjTitle").get_text().replace(" ", ""), "urls" : "https://www.release.tdnet.info/inbs/"+j.find("a").get("href"), 
                "script" : " "})
            else : 
                result.append({"codes" : j.find(attrs = "oddnew-M kjCode").get_text(), "names" : j.find(attrs = "oddnew-M kjName").get_text().replace(" ", ""), 
                "date" : today, "titles" : j.find(attrs = "oddnew-M kjTitle").get_text().replace(" ", ""), "urls" : "https://www.release.tdnet.info/inbs/"+j.find("a").get("href"), 
                "script" : " "})

    logger.info("end geturl")

    return result

#pdfファイルを読んでStringに変換して返す関数。
def readpdfs(result):
    logger.info("start readpdf")
    for link in result:

        tempfiles = urlopen(link['urls']).read()
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

        temp = temp.replace("  ", "")
        temp = temp.replace("\n\n", "\n")

        link["script"] = temp

        retstr.close()
    logger.info("end readpdf")
    return result

#DBにDataを保存する関数。
def savedb(result):
    logger.info("start savedb")
    today = str(datetime.date.today().strftime("%Y%m%d"))
    clients = MongoClient("mongodb://root:example@localhost:27017/") #db connect
    db = clients.mongo_crontab #db指定
    n = 1
    for result in result : 
        datas = {
            "_id" : today+"-"+str(n),

            "compy" : { 
                "code" : result["codes"], 
                "name" : result["names"] 
            },

            "date" : result["date"],

            "document" : { 
                "link" : result["urls"], 
                "title" : result["titles"],
                "script" : result["script"]
            }
        }
        db.tdnet.insert_one(datas)
        n += 1


    logger.info("end savedb")

if __name__ == "__main__" :
    logger.info("start mongo crawling")
    result = geturls()
    readpdfs(result)
    savedb(result)
    logger.info("end mongo crawling")


