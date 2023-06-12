import secrets
from api_writewise.db import mongo
from bson import ObjectId
import bcrypt

class User:
    collection = mongo.MONGODB_DB['users']

    @classmethod
    def create(cls, data):
        # password = data['password'].encode('utf-8')
        # hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # data['password'] = hashed_password
        return cls.collection.insert_one(data)

    @classmethod
    def get_by_email(cls, email):
        return cls.collection.find_one({'email': email})

    @classmethod
    def get_by_id(cls, user_id):
        return cls.collection.find_one({'_id': ObjectId(user_id)})
    
    @classmethod
    def generate_password_reset_token(cls, user_id):
        token = secrets.token_hex(20)
        cls.collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'password_reset_token': token}})
        return token

