TDnetのPDFファイルをcrawlingするprogram
===========


## 内容
* TDnet siteでその日にuploadされるPDFで作成された企業の情報をcrawlingしてMongoDBに保存する。

## 実行法
* mongocrawling.pyを起動することで作動。

## DB
* documentの仕組み

        "_id" : "日付-番号(1から)",
        "compy" : {
            "code" : "会社のcode",
            "name" :　"会社の名前"
        },
        "date" : "日付",
        "document" : {
            "link" : "資料のウェブ注所", 
            "title" : "資料のtitle",
            "script" : "資料の内容"
        }

## 出力結果
![DB](https://github.com/SangWooChun714/mirineglobal/blob/master/mgproject/DBkey.JPG)


## crontabの設定
