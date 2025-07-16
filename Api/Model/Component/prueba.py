from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client['LlamaWeb']
collection = db['llamaConsumption']

# Buscar solo documentos donde consDay sea string
cursor = collection.find({"consDay": {"$type": "string"}})

for doc in cursor:
    try:
        fecha_str = doc['consDay']
        # Convertir solo la fecha y agregar hora 00:00:00 automáticamente
        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d')

        collection.update_one(
            {'_id': doc['_id']},
            {'$set': {'consDay': fecha_dt}}
        )
    except Exception as e:
        print(f"Error con _id {doc['_id']}: {e}")
