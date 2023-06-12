import pymongo


MONGODB_HOST = 'mongodb+srv://admin:uINsqkhy8mrC4rv2@clusterchanblock.9rmo2.mongodb.net/?retryWrites=true&w=majority'
MONGODB_CLIENT = pymongo.MongoClient(MONGODB_HOST)
MONGODB_DB = MONGODB_CLIENT["userWriteWise"]
MONGODB_DB_SAVE_REPORT = MONGODB_CLIENT["historical_report_writewise"]


