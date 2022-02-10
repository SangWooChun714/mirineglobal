from cgitb import html
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from selenium import webdriver

search = input("검색어")
url = "https://www.google.com/search?q="+search+"&sxsrf=APq-WBvtfFoXTXBiJB93nPwcIcG-0Rxq_A:1644472515014&source=lnms&tbm=isch&sa=X&ved=2ahUKEwizkObAufT1AhXTZN4KHZKeDlwQ_AUoAXoECAEQAw&biw=2560&bih=1297&dpr=1"

driver = webdriver.Chrome()
driver.get(url)
for i in range(500):
    driver.execute_script("window.scrollBy(0,10)")

html = driver.page_source
soup = BeautifulSoup(html)
img = soup.select("img")
n = 1
imgurl = []

for i in img:
    try:
        imgurl.append(i.attrs["src"])
    except KeyError:
        imgurl.append(i.attrs["data-src"])

for i in imgurl:
    urlretrieve(i,"C:/Users/csw/Desktop/mirineglobal/pythonfile/img/"+search+str(n)+".jpg")
    n += 1
driver.close()