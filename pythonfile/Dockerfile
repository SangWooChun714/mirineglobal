FROM python:3.7-slim-stretch

WORKDIR /pythonfile

COPY kabusavecsv.py /pythonfile/
COPY drawfin.py /pythonfile/
COPY kabuconfig.py /pythonfile/
COPY 상장법인목록.xlsx /pythonfile/
COPY requirements.txt /pythonfile/

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt



