from matplotlib.pyplot import text
import requests, datetime
from bs4 import BeautifulSoup
from io import StringIO
import requests, datetime
from bs4 import BeautifulSoup
from pdfminer.pdfinterp import PDFResourceManager, PDFPage, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import BytesIO
from urllib.request import urlopen
import pdfplumber



    
yesterday = str(datetime.date.today()-datetime.timedelta(1))    
today = str(datetime.date.today().strftime("%Y%m%d"))
#'https://www.release.tdnet.info/inbs/I_list_00+'+6+'_20220516.html'
tempurl = "https://www.release.tdnet.info/inbs/I_list_001_20220516.html"
#url = "https://www.release.tdnet.info/inbs/I_list_001_"+today+".html"
headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}#heaaderを指定
#headers = {"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}#heaaderを指定
requst = requests.get(url=tempurl, headers=headers)
searchurl = BeautifulSoup(requst.text, "lxml")
tablenum = searchurl.find_all("div", attrs={"class" : "pager-M"})
#print(tablenum[-1].get_text())
tablenum = tablenum[-1].get_text()
tempurl = searchurl.find_all("td", attrs={"class" : "oddnew-M kjTitle"})
urls = []
i = 0
for j in tempurl:
        urls.append("https://www.release.tdnet.info/inbs/"+j.find("a").get("href"))
        #urls[i] = "https://www.release.tdnet.info/inbs/"+urls[i]
        # print(i)
        print(urls[i])
        i += 1
i = 0
content = []
for link in urls:
    tempfiles = urlopen(link).read()
    files = BytesIO(tempfiles)

    output_string = StringIO()
    parser = PDFParser(files)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    content = output_string.getvalue()
    content = content.replace("\n\n", "")
    print(content)
    break