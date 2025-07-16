from Api.Entity import User
import Api.Model.Component.componentLogin as dao

class ModelLogin():

    def __init__(self):
        pass

    def getValidateUser(self,user:User,db):  
        response,data,status = dao.getValidateUser(user,db)              
        return data,status
