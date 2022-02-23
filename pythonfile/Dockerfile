FROM python:3

RUN mkdir /pythonfile

WORKDIR /pythonfile

COPY kabusavecsv.py /pythonfile/
COPY drawfin.py /pythonfile/
COPY kabuconfig.py /pythonfile/
COPY 상장법인목록.xlsx /pythonfile/

RUN pip install lxml
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install bs4
RUN pip install openpyxl
RUN pip install matplotlib
RUN pip install requests

CMD [ "python", "kabusavecsv.py", "카카오게임즈", "2022.01.15" ]

