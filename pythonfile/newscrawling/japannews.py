from asyncio.log import logger
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import ssl
from newscofig import logger
from elasticsearch import Elasticsearch
from datetime import date


def japannews():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    chrome_service = Service(executable_path="C:/Users/mg-e1/Desktop/mg/chromedriver.exe")
    driver = webdriver.Chrome(service=chrome_service, options=options)

    driver.get()
    print("news")


if(__name__ == "__main__"):
    logger.info("start japan news")
    japannews()
    logger.info("end japan news")
p