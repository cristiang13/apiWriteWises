from api_writewise.db import mongo
from bson import ObjectId
import bcrypt

class HistoricalReportMongo:
    collection = mongo.MONGODB_DB_SAVE_REPORT['historical_report']

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_by_id(cls, historical_id):
        return cls.collection.find_one({'_id': ObjectId(historical_id)})
    
    @classmethod
    def get_by_user_id(cls, user_id):
       return cls.collection.find( {"user_id": user_id})
