import csv
import matplotlib
import matplotlib.pyplot as plt


matplotlib.rc("font", family="Malgun Gothic")

kabulist = []
days = []
price = []
qunt = []
name = ""

def drawline(filename):
    with open(filename, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        kabulist = list(reader)
        f.close()
    name = kabulist[1][0].split("(")[0]

    for i in range(len(kabulist)-1, 0, -1):
    # for i in range(1, len(kabulist)):
        for j in range(1, 4):
            if j == 1 :
                days.append(kabulist[i][j]) 
            elif j == 2:
                price.append(kabulist[i][j])
            elif j == 3:
                qunt.append(kabulist[i][j])

    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(price, color = "green", marker="o", label="주가")
    plt.plot(qunt, color="red", marker="o", label="거래량")
    plt.xticks(range(len(days)), days, rotation=45)
    plt.title(name)
    plt.legend()
    plt.show()