from datetime import datetime,timedelta
import Api.Model.Component.componentGeneral as gen
from bson import ObjectId
def getInfoIncomePredict(income,idIncome,db):
    try:
        response    =   dict(status=200, mensaje= "Todo bien ")
        ListActiva  =   gen.getInfoIncomePredictActive(income,db)
        setDataBase =   []
        day         =   income.incDateF - income.incDateI
        count       =   day.days
        mount       =   income.incAmount/count 
        for x in range(0,count):
            dayCompare  =   income.incDateI+timedelta(days=x)
            registro    =   0
            if ListActiva != []: 
                for index, y in enumerate(ListActiva): 
                    if y[1].date() == dayCompare.date() : 
                        r           =   gen.updateInfoIncomePredictActive(y,mount,db)
                        registro    =   1                    
                        if r['status'] != 200:
                            return r 
                        break
            if registro == 0:
                DictData      = {}
                DictData['idIncome']    =  ObjectId(idIncome)
                DictData['idUser']      =  ObjectId(income.idUser)
                DictData['preDate']     =  income.incDateI+timedelta(days=x)
                DictData['preAmountP']  =  mount  
                DictData['preAmountR']  =  0
                setDataBase.append(DictData)
        if setDataBase != []:
            response    =  gen.setInfoIncomePredict(setDataBase,db)
        return response
    except Exception as e:
        response['statu']    =   500
        response['mensaje']  =  f"error: {str(e)}"
        return  response
