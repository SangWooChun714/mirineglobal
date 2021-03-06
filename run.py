from flask import Flask, render_template, request
from pymysql import NULL
from pythonfile.newscrawling import searchnetwork



app = Flask(__name__)

@app.route("/")#웹 브라우저에서 웹서버로 접근 시 / 가 입력되면 이 함수가 실행되도록 함.
def hello_World():
    return render_template('kabu.html') # flask의 함수로 templates 폴더 내의 해당 파일을 찾아가도록 해준다.

@app.route("/search", methods=["POST"]) # /search 가 입력되면 이 함수를 실행하고 내용을 post방식으로 받아온다
def searchkabuweb():
    if request.form['kabuname'] == "":
        search = "search is empty"
        print("succes")
    else : 
        search = request.form['kabuname'] # 서버의 request에서 kabuname이라는 변수를 받아온다 이것은 html의 name태그를 지정하여 받아온다.
    print(search+" 1")
    files = searchnetwork.wordcloudmethod(search)
    #result = searchkabu.searchkabu(kabuname) #pythonfile 폴더의 searchkabu.py를 import하여 파일 내부의 searchkabu라는 함수에 kabuname을 넣어 결과를 result에 저장
    # code = result[0] # 상장된 회사의 코드
    # nowval = result[1] # 현재 주식 가격
    # qunt = result[2] # 주식의 거래량
    # upper = result[3] # 전날에 비해 상승인지 하락인지를 나타냄
    # differ = result[4] # 전날에 비교한 가격변동
    #return render_template("search.html", kabuname = kabuname, Code = code, Nowval = nowval, Qunt = qunt, Upper = upper, Differ = differ) 
    return render_template("search.html", filenames = 'image/'+files, search = search )
    # templates 폴더 내부의 search.html 로 이동하며 request에 변수를 넣어줌

app.run(host="localhost", port=2500) # 서버 시작코드
