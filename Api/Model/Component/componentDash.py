from pymongo.errors import PyMongoError
import traceback
from bson import ObjectId


def GetDataConsumption(idUser, conn):
    try:
        respuesta   =   []
        collection  =   conn['llamaConsumption']
        cursor      =   collection.find({'idUser':ObjectId(idUser.user)})
        if cursor:
            for x in cursor:
                data ={
                    'Fecha':x['consDay'],
                    'Monto':x['consDiner'],
                    'Tipo':x['consTyPay'],
                    'Producto':x['consProd'],
                    'Tarjeta':x['consCard']
                }
                respuesta.append(data)

        return respuesta
    except Exception as e:
        raise([f'Error {traceback.format_exc()}'])
