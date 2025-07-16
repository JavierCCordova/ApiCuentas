from pymongo.errors import PyMongoError
import traceback
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime

def getEstablishments(db):
    try:
        response    = []
        collection  = db['llamaEstablishment']
        cursor      = collection.find()
        for x in cursor:
            response.append(x.get('estaName',''))

        return 200,response
    except ConnectionError as e:
        print(f"Errore de DDBB: {str(traceback.format_exc())}")
        return 500,[f"Errore de inesperado: {str(traceback.format_exc())}"]
    except PyMongoError as e:
        print(f"Errore de Pymongo: {str(e)}")
        return 500, [ f"Errore de inesperado: {str(traceback.format_exc())}"]
    except Exception as e:
        print(f"Errore de inesperado: {str(e)}")
        return 500,[f"Errore de inesperado: {str(traceback.format_exc())}"]
    

def getCards(db,form):
    try:
        response    = []
        collection  = db['llamaCards'] 
        cursor      = collection.find({'idUser':ObjectId(form.user)})
        for x in cursor:
            data                = {}
            data['cardName']    = x.get('cardName','')
            data['cardType']    = x.get('cardType','')

            response.append(data)

        return 200,response
    except ConnectionError as e:
        print(f"Errore de DDBB: {str(traceback.format_exc())}")
        return 500,[f"Errore de inesperado: {str(traceback.format_exc())}"]
    except PyMongoError as e:
        print(f"Errore de Pymongo: {str(e)}")
        return 500, [ f"Errore de inesperado: {str(traceback.format_exc())}"]
    except Exception as e:
        print(f"Errore de inesperado: {traceback.format_exc()}")
        return 500,[f"Errore de inesperado: {str(traceback.format_exc())}"]
    
def setFormConsumption(db,form):
    try:
        formDict    = form.model_dump()
        formDict['idUser']  =   ObjectId(formDict['idUser'])
        formDict['consDay'] =   datetime.strptime(formDict['consDay'], '%Y-%m-%d')
        collection  = db['llamaConsumption']
        cursor      = collection.insert_one(formDict)
        if cursor:
            return {"status":200,"detail":"Se inserto"}
        else:
            return {"status":500,"detail":"No llego insertar"}
    except Exception as e:
        print(f"problema: {traceback.format_exc()}")
        return {"status":500,"detail":"Problemas del server"}

    
def setFormCard(db,card):
    try:
        formDict    = card.model_dump()
        formDict['idUser']      =   ObjectId(formDict['idUser'])
        formDict['cardBool']    =   1 
        collection  = db['llamaCards']
        cursor      = collection.insert_one(formDict)
        if cursor:
            return {"status":200,"detail":"Se inserto"}
        else:
            return {"status":500,"detail":"No llego insertar"}
    except Exception as e:
        print(f"problema: {traceback.format_exc()}")
        return {"status":500,"detail":"Problemas del server"}
    
    
def setFormEstablisment(db,esta):
    try:
        formDict    = esta.model_dump()  
        collection  = db['llamaEstablishment']
        cursor      = collection.insert_one(formDict)
        if cursor: 
            return {"status":200,"detail":"Se inserto"} 
        else:
            return {"status":500,"detail":"No llego insertar"}
    except Exception as e:
        print(f"problema: {traceback.format_exc()}")
        return {"status":500,"detail":"Problemas del server"}
    
    
def setFormIncome(db,income):
    try:
        formDict    = income.model_dump()  
        formDict['idUser'] = ObjectId(formDict['idUser'])
        collection  = db['llamaIncome']
        cursor      = collection.insert_one(formDict)
        if cursor:
            return {"status":200,"detail":"Se inserto"},cursor.inserted_id
        else:
            return {"status":500,"detail":"No llego insertar"},0
    except Exception as e:
        print(f"problema: {traceback.format_exc()}")
        return {"status":500,"detail":"Problemas del server"},0