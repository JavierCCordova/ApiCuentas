import traceback
from datetime import datetime,timedelta
import calendar
from bson import ObjectId

def getConsumptionmonth(idUser,db):
    try:
        response    =   []
        responseDa  = dict(status= 200 , data = {})  
        hoy         = datetime.now()
        inicio      = hoy.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
        ultimo      = calendar.monthrange(hoy.year, hoy.month)[1] 
        final       = hoy.replace(day=ultimo,hour=23)

        collection  = db['llamaConsumption']  
        cursor      = collection.find({
                            'idUser':ObjectId(idUser.user),
                            "consDay": {
                                "$gte": inicio,
                                "$lte": final
                            }
                        })
        if cursor: 
            for x in cursor:
                tipo = {
                    'id': str(x.get('_id','')),
                    'Fecha': datetime.strftime(x.get('consDay',''),'%Y-%m-%d'),
                    'Monto': x.get('consDiner',''),
                    'Tipo': x.get('consTyPay',''),
                    'Producto': x.get('consProd',''),
                    'Tarjeta': x.get('consCard',''),
                }  
                response.append(tipo)
         
        return response
    except Exception as e:
        return {'status':200,'data':f'Error {str(e)}'}
    

def setConsumptionDelete(consump:str,db):
    try:
        response    = dict(status = 200,detail= '')
        collection  = db['llamaConsumption']
        cursor      = collection.delete_one({'_id':ObjectId(consump.idConsumption)})
        if cursor.deleted_count ==0:
            response['status']  = 500
            response['detail']  = 'No se encontro el ID'
        else:
            response['status']  = 200
            response['detail']  = 'realizado'
        return response 
    except Exception as e:
        response['status']  = 500
        response['detail']  = f'se tuvo un error al {str(e)}'
        return response
