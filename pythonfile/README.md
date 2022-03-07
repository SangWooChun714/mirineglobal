株価をcrawlingしてグラフを描くコード
===========


## 内容
* 会社の名前と検索したい日付を入力すれば入力した日から昨日までの株価と取引量をcsvファイルにしてグラフを出力します。

## 実行法
* kabusavecsv．py　'会社の名前' '日付（yyyy．㎜．dd）'をコマンドで入力

例

    kabusavecsv.py '삼성전자' '2022.01.01'
    kabusavecsv.py '카카오게임즈' '2022.1.1'

## 出力結果
* csvファイルは'주식이력.csv'で貯蔵します。

例

    주식이력.csv

* ogはkabulog.logで貯蔵します。

screenshot

![csv](https://github.com/SangWooChun714/mirineglobal/blob/master/pythonfile/csvfile.JPG)

![graph](https://github.com/SangWooChun714/mirineglobal/blob/master/pythonfile/%EA%B1%B0%EB%9E%98%EB%9F%89EX.jpg)
