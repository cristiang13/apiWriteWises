from django.db import models
import secrets
from api_writewise.db import mongo
from bson import ObjectId

# Create your models here.
class Childs:
    # collection = mongo.MONGODB_DB['users']
    collection = mongo.MONGODB_DB['childs']
    

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data)
    
    @classmethod
    def get_by_childcareworker(cls, childcareworker_id):
        childs = cls.collection.find({'childcare_worker': childcareworker_id})
         # Convertir cursor de MongoDB a lista de diccionarios
        childs = list(childs)

        # Convertir ObjectId a string para serialización de JSON
        for child in childs:
            child['_id'] = str(child['_id'])
        return [doc for doc in childs]
    