from app.models.config_reader import ConfigReader
from app.models.indexer import Indexer
from app.models.ranker import Ranker
from lib.database.connector import AccessDatabase
from pyvi import ViTokenizer
import time

class Main:

    def __init__(self):
        configer = ConfigReader("./app/config/service.conf")
        configer.parseFile()
        configInfo = configer.config
        dbHost, dbPort, dbName = configInfo["dbHost"], configInfo["dbPort"], configInfo["dbName"]
        accessor = AccessDatabase(dbHost, dbPort, dbName)

        fields = {
            "title" : 1.0,
            "content" : 0.7
        }
        indexer = Indexer(accessor, fields, 0.2)
        start = time.time()
        query = ViTokenizer.tokenize("ma chơi ở nauy")
        rData = indexer.retrieval(query, query.split(), ["Người ngoài hành tinh", "Ngày tận thế", "1001 bí ẩn", "Chinh phục sao Hỏa"])
        print("Done! %.2f" % (time.time() - start))

        start = time.time()
        ranker = Ranker()
        ranker.setData(query, rData, fields)
        ranker.getResult()
        print("Done! %.2f" % (time.time() - start))


if __name__ == "__main__":
    Main()