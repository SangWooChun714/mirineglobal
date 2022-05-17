import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s- %(funcName)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("C:/Users/mg-e1/Desktop/mg/mgproject/mongo.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)