from asyncio.log import logger
import csv
import matplotlib
import matplotlib.pyplot as plt


matplotlib.rc("font", family="Malgun Gothic")

kabulist = [] # csv에서 나온 파일을 저장할 변수
days = [] # 날짜를 저장할 변수
price = [] # 종가를 저장할 변수
qunt = [] #거래량을 저장할 변수
name = "" #회사이름을 저장할 변수

def drawline(filename):
    with open(filename, "r", encoding="utf-8-sig") as f: #csv파일을 불러옴
        logger.info("open csv file")
        reader = csv.reader(f)
        kabulist = list(reader)
        f.close()
    name = kabulist[1][0].split("(")[0] #회사 이름이 회사이름(코드) 형식으로 저장되어있어 이름만을 잘라내어 저장

    for i in range(len(kabulist)-1, 0, -1): # 그래프는 과거~현재로 나와야 하고, csv파일은 현재~과거 순으로 저장되어 있어 역순으로 출력
    # for i in range(1, len(kabulist)):
        for j in range(2, 5):
            if j == 2 :
                days.append(kabulist[i][j]) 
            elif j == 3:
                price.append(kabulist[i][j])
            elif j == 4:
                qunt.append(kabulist[i][j])
    logger.info("over file work start draw")
    
    fg = plt.figure(figsize=(12,9)) #그래프를 그릴 종이를 설정
    fg.add_subplot(1, 2, 1) # 그래프를 2개 그리며, 그중 첫번째 그래프
    plt.plot(days, price, color = "green", marker="o", label="kabuka") # 그래프에 그려질 내용, 종가를 표시
    plt.legend() # 그래프의 주석
    plt.xticks(range(len(days)), label=days ,rotation=45) #x축의 설정
    fg.add_subplot(1, 2, 2) # 두 번째 그래프로 거래량을 표시
    plt.plot(days, qunt, color="red", marker="o", label="volume")
    plt.legend()
    plt.xticks(range(len(days)), label=days ,rotation=45) #x축의 설정
    logger.info("draw over show")
    plt.show() # 그래프를 표시
    plt.savefig("kabu.jpg")
    print("painting over")