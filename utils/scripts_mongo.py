import pymongo
import bcrypt

MONGODB_HOST = 'mongodb+srv://admin:uINsqkhy8mrC4rv2@clusterchanblock.9rmo2.mongodb.net/?retryWrites=true&w=majority'
# MONGODB_CLIENT = pymongo.MongoClient(MONGODB_HOST)
# MONGODB_DB = MONGODB_CLIENT["userWriteWise"]
# Reemplaza con los valores de tu base de datos

# Conexión a MongoDB
client = pymongo.MongoClient(MONGODB_HOST)


# buscar todos los usuarios
def find_all_users():
    db_name = "userWriteWise"
    collection_name = "userstest"
    db = client[db_name]
    collection = db[collection_name]
    users = collection.find()
    # Consulta todos los documentos de usuarios en la colección
    collection.update_many(
        {},
        {
            "$set": {
                "last_email_sent": None
            }
        }
    )
    # Cierra la conexión a MongoDB
    client.close()

# Recorre cada documento y encripta el password
# for user in users:
#     plain_password = user["password"]
#     hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())

#     # Actualiza el documento con el nuevo password encriptado
#     collection.update_one(
#         {"_id": user["_id"]},
#         {"$set": {"password": hashed_password.decode("utf-8")}}
#     )

def update_historical_report():
    print("actualizando datos reportes historicos")
    db_name = "historical_report_writewise"
    collection_name = "historical_report"
    db = client[db_name]
    collection = db[collection_name]
    
    default_goalObservations = "Not available"
    default_goal_follow_up = "Not available"
    default_range_age_daily_report = "Not available"
    default_range_age = "Not available"
    
    # Crea los valores por defecto para el nuevo campo "child" 
    default_child = {
        'child_id': 'default_id',
        'child_name': 'default_name',
        'child_age': 'default_age',
    }
    
    collection.update_many(
        {
            'type_report': {'$in': ['follow_up', 'descriptions_report', 'goal_report']},
            'child': {'$exists': False}
        },
        {
            '$set': {'child': default_child}
        }
    )
    # collection.update_many(
    #     {
    #         'type_report': 'descriptions_report',
    #         'child': {'$exists': False}
    #     },
    #     {
    #         '$set': {'child': default_child}
    #     }
    # )

     # Agrega el campo "goalObservations" a los documentos que no lo tengan
    collection.update_many(
        {
            'type_report': 'descriptions_report',
            'goalObservations': {'$exists': False}
        },
        {
            '$set': {'goalObservations': default_goalObservations}
        }
    )       
    
    collection.update_many(
        {
            'type_report': 'follow_up',
            'goal': {'$exists': False}
        },
        {
            '$set': {'goal': default_goal_follow_up}
        }
    )
    
    collection.update_many(
        {
            'type_report': 'daily_report',
            'rangeAge': {'$exists': False}
        },
        {
            '$set': {'rangeAge': default_range_age_daily_report}
        }
    )
    
    collection.update_many(
        {
            'type_report': 'weekly_planning',
            'rangeAge': {'$exists': False}
        },
        {
            '$set': {'rangeAge': default_range_age_daily_report}
        }
    )
    
    print("finalizacion de actualizacion datos reportes historicos")
    
     # Cierra la conexión a MongoDB
    client.close()

update_historical_report()