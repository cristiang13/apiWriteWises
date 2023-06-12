import os
import pymongo
from dotenv import load_dotenv
load_dotenv()


MONGODB_HOST = os.getenv("MONGODB_HOST")
MONGODB_CLIENT = pymongo.MongoClient(MONGODB_HOST)
MONGODB_DB = MONGODB_CLIENT["userWriteWise"]
MONGODB_DB_SAVE_REPORT = MONGODB_CLIENT["historical_report_writewise"]


