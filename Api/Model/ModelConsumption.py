import Api.Model.Component.componentConsumption as consumo

class ModelConsumption():

    def __init__(self):
        pass

    def getConsumptionmonth(self,idUser,db): 
        responseData         = dict(status = 200, data = {})
        response             = consumo.getConsumptionmonth(idUser,db)
        responseData['data'] = response
        return responseData
    
    def setConsumptionDelete(self,idConsumption:str,db):
        response            = consumo.setConsumptionDelete(idConsumption,db)
        return response