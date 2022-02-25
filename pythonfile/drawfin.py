from asyncio.log import logger
import csv
import matplotlib
import matplotlib.pyplot as plt


matplotlib.rc("font", family="Malgun Gothic")#韓国語を表示するコード

#graphを描く関数
def drawline(filename):
    kabulist = [] # csvの資料を保存
    days = [] # 日を保存
    price = [] # 株価を保存
    qunt = [] #　取引量を保存
    with open(filename, "r", encoding="utf-8-sig") as f: #csvファイルを読む
        logger.info("open csv file")
        reader = csv.reader(f)
        kabulist = list(reader)
        f.close()

    for i in range(len(kabulist)-1, 0, -1): # graphを日付順に作成するための逆に読む
    # for i in range(1, len(kabulist)):
        for j in range(2, 5):
            if j == 2 :
                days.append(kabulist[i][j]) 
            elif j == 3:
                price.append(kabulist[i][j])
            elif j == 4:
                qunt.append(kabulist[i][j])
    logger.info("over file work start draw")
    
    fg = plt.figure(figsize=(12,9)) #graphの紙を設定
    fg.add_subplot(1, 2, 1) # graphを二つ描いてその最初のgraphを設定
    plt.plot(days, price, color = "green", marker="o", label="kabuka") # 株価を表示
    plt.legend() #
    plt.xticks(range(len(days)), label=days ,rotation=45) #x축의 설정
    fg.add_subplot(1, 2, 2) # 二番graph取引量を表示
    plt.plot(days, qunt, color="red", marker="o", label="volume")
    plt.legend()
    plt.xticks(range(len(days)), label=days ,rotation=45) #x軸日付で設定
    logger.info("draw over show")
    plt.show() # graphの表示
    plt.savefig("kabu.jpg")#graphの保存
    print("painting over")