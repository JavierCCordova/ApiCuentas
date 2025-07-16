from bson import ObjectId
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import traceback

def getDetailData(idUser,conn):
    try:
        response    =   [] 
        responseT   =   [] 
        responseD   =   dict(status= 200)  
        collection  =   conn['llamaConsumption']
        now         =   datetime.now()
        inicio      =   now.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
        inicio      =   inicio - relativedelta(months=2)
        ultimo      =   calendar.monthrange(now.year, now.month)[1] 
        final       =   now.replace(day=ultimo,hour=23)
        cursor      =   collection.find({
                            'idUser':ObjectId(idUser.user),
                            "consDay": {
                                "$gte": inicio,
                                "$lte": final
                            } })
        if cursor:
            for x in cursor:
                tipo = { 
                        'Fecha': datetime.strftime(x.get('consDay',''),'%Y-%m-%d'),
                        'Monto': x.get('consDiner',''),
                        'Tipo': x.get('consTyPay',''), 
                        'Tarjeta': x.get('consCard',''),
                        'Cuota': x.get('consCouta',0),
                    }  
                response.append(tipo)

        cursor2     =   conn['llamaCards'].find()
        if cursor2:
            for x in cursor2:
                tipo2 = {
                        'Tarjeta':x.get('cardName',''),
                        'TipoTar':x.get('cardType',0),
                        'Inicio':x.get('cardFIni',0),
                        'Fin':x.get('cardFEnd',0),
                        'Pago': round(x.get('cardFPay',0),ndigits=2),
                }
                responseT.append(tipo2)

        responseD['data']   =   response
        responseD['dataT']  =   responseT 
        return responseD
    except Exception as e:
        responseD['status'] = 500
        responseD['Error']  = f'Error inesperado: {str(e)}'
        return responseD
    
def getIncomeActive(idUser,conn):
    try:
        ResponseList    =   []
        ResponseListP   =   []
        day             =   datetime.now() 
        collection      =   conn['llamaIncome']
        startDay        =   datetime.combine(day.date(),datetime.min.time())
        filtroData      =   {
                                "idUser"  : ObjectId(idUser.user),
                                "incDateI": { "$lte": startDay },
                                "incDateF": { "$gte": startDay }
                            }
        cursor          =   collection.find(filtroData)
        if cursor:
            for   x   in cursor:                
                ResponseList.append( ObjectId(x.get('_id','')) ) 
 
        collection2     =   conn['llamaIncomePredict']
        filtroPre       =   {   "idIncome" :    {  "$in": ResponseList }   }
        cursor          =   collection2.find(filtroPre)
        if cursor:
            for y in cursor:
                data            =   {}
                data['Monto']   =   round(y.get('preAmountP',0.0),ndigits=2)
                data['Date']    =   datetime.strftime(y.get('preDate'),'%Y-%m-%d')
                data['idIncome']=   y.get('idIncome','')
                ResponseListP.append(data)
        return ResponseListP
    except Exception as e: 
        print(traceback.format_exc())
        return []