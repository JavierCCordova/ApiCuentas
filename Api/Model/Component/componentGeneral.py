from pymongo import MongoClient
import traceback
from bson import ObjectId

def setInfoIncomePredict(ListData,db):
    try:
        collection  =   db['llamaIncomePredict']
        cursor      =   collection.insert_many(ListData) 
        if cursor: 
            return {"status":200,"detail":"Se inserto"} 
        else:
            return {"status":500,"detail":"No llego insertar"}
    except Exception as e:
        print(f"problema: {traceback.format_exc()}")
        return {"status":500,"detail":"Problemas del server"}
    
def getInfoIncomePredictActive(income,db):
    try:
        idsColecti  =   []
        collection  =   db['llamaIncomePredict']
        cursor      =   collection.find({
            'idUser':ObjectId(income.idUser),
            "preDate": {
                        "$gte": income.incDateI.replace(day=1,hour=0,minute=0,second=0,microsecond=0),
                        "$lte": income.incDateF.replace(hour=23)
                                        } 
        }) 
        if cursor:
            for x in cursor:
                data  =   (x.get('_id',''),x.get('preDate',''),x.get('preAmountP',0))
                idsColecti.append(data)
            return idsColecti
        else:
            return idsColecti
    except Exception as e:        
        return []
    
def updateInfoIncomePredictActive(y,mount,db):
    try:
        idsColecti  =   []
        collection  =   db['llamaIncomePredict']
        search      =   {'_id':ObjectId(y[0])}
        update      =   {'$set':{"preAmountP": (y[2]+mount)}}
        cursor      =   collection.update_one(search, update) 
        if cursor:
            return {"status":200,"detail":"Se inserto"} 
        else:
            return {"status":500,"detail":"No llego insertar"}
    except Exception as e:        
        return {"status":500,"detail":"Problemas del server"}