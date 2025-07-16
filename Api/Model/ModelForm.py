import Api.Model.Component.componentForm as dao
import Api.Model.ModelGeneral as gen

class ModelForm():

    def __init__(self):
        pass

    def getFormlist(self,db,form):  
        response                    = self.getResponse()
        response['establishment']   = self.getEstablishments(db=db)
        response['cards']           = self.getCards(db=db,form=form)        
        return response['status'],response

    def getEstablishments(self,db):
        status, response = dao.getEstablishments(db=db)
        if status == 200:
            return response
        else:
            return status
    
    def getCards(self,db,form):
        status,response = dao.getCards(db=db,form=form)
        if status == 200:
            return response
        else:
            return status
    
    def getResponse(self):
        return {'status': 200}
    
    def setFormConsumption(self,db,form):
        response = dao.setFormConsumption(db=db,form=form)
        return response
    
    def setFormCard(self,db,card):
        response = dao.setFormCard(db=db,card=card)
        return response 
    
    def setFormEstablishment(self,db,esta):
        response = dao.setFormEstablisment(db=db,esta=esta)
        return response 
    
    def setInconme(self,db,income):
        response, idIncome    = dao.setFormIncome(db=db,income=income)
        if response['status'] == 200:
            response2   =   gen.getInfoIncomePredict(income,idIncome,db)
            if response2['status'] != 200:
                return response2
        return response 