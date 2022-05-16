from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO, open
from urllib.request import urlopen

pdffile = urlopen("https://www.release.tdnet.info/inbs/140120220513547791.pdf")
#pdffile = open("C:/Users/mg-e1/Desktop/mg/pdftest.pdf", "rb")
rsrcmgr = PDFResourceManager()
retstr = StringIO()
laparams = LAParams()
device = TextConverter(rsrcmgr, retstr, laparams=laparams)

process_pdf(rsrcmgr, device, pdffile)
device.close()

content = retstr.getvalue()
retstr.close()
print(content)