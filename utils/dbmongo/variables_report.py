from api_writewise.db import mongo
from bson import ObjectId
import bcrypt

class VariablesReport:
    collection = mongo.MONGODB_DB_SAVE_REPORT['variables_report']

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_by_id(cls, document_id):
        return cls.collection.find_one({'_id': ObjectId(document_id)})
    
    @classmethod
    def get_by_user_id(cls, user_id):
       return cls.collection.find( {"user_id": user_id})
   
    @classmethod
    def get_last_doc(cls, user_id, type_report):
        documents = cls.collection.find({"user_id": user_id, "type_report": type_report}).sort("timestamp", -1).limit(1)
        # return cls.collection.find_one({"user_id": user_id, "type_report": type_report}).sort([("timestamp", -1)]).limit(1)
        return documents[0] if documents else None 