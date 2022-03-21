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
* csvファイルは'会社の名前.csv'で貯蔵します。

例

    주식이력.csv

* logはkabulog.logで貯蔵します。

screenshot

![csv](https://github.com/SangWooChun714/mirineglobal/blob/master/pythonfile/csvfile.JPG)　![graph](https://github.com/SangWooChun714/mirineglobal/blob/master/pythonfile/%EA%B1%B0%EB%9E%98%EB%9F%89EX.jpg)


## dockerの実行
* cmdでdocker-composeファイルがあるフォルダに入って　'docker-compose up --build' を入力してcontainerを作って起動させる。

screenshot
![docker](https://github.com/SangWooChun714/mirineglobal/blob/master/pythonfile/docker.JPG)

* dockerのcontainerが起動したらcmdで　'docker exec -it python3 /bin/bash'　を入力してcontainerの中に入る。

![docker](https://github.com/SangWooChun714/mirineglobal/blob/master/pythonfile/dockerbash.JPG)

* container入ったら　'python kabusavecsv.py 会社の名前　日付' で株価を見たい会社と日を入力する。

![docker](https://github.com/SangWooChun714/mirineglobal/blob/master/pythonfile/container.JPG)

* programの起動に成功したらlog,jpg,csvファイルが生成される。

![docker](https://github.com/SangWooChun714/mirineglobal/blob/master/create_file.JPG)　![docker](https://github.com/SangWooChun714/mirineglobal/blob/master/log.JPG)
