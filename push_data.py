import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo

from dotenv import load_dotenv

from networksecurity.exception.exception import NetworkSecurityException

load_dotenv()

MONGO_DB_URI = os.getenv("MONGODB_URI")
print(f"MongoDB URI: {MONGO_DB_URI}")

ca = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, csv_file_path: str):
        try:
            data = pd.read_csv(csv_file_path)
            data.reset_index(drop=True, inplace=True)
            records = json.loads(data.T.to_json()).values()
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI, tlsCAFile=ca)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return ("Data inserted successfully", len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = r"Network_Data\phisingData.csv"
    DATABASE = "network-security"
    COLLECTION = "Network_Data"
    networkobject = NetworkDataExtract()
    records = networkobject.csv_to_json_converter(FILE_PATH)
    print(records)
    no_of_records = networkobject.insert_data_to_mongodb(records, DATABASE, COLLECTION)
    print(no_of_records)
