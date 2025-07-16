from pymongo import MongoClient,errors
from decouple import config

class Conexion:
    def __init__(self):
        self.userM = config('APIMONGODB') #  'localhost'
        self.passM = ''
        self.servM = ''
        self.dbasM = config('APICOLLECTION')#'LlamaWeb'
        self.clien = None
        self.db    = None

    def getConexion(self):
        try:
            mongoUrl    = self.userM    #f'mongodb://{self.userM}:27017/'
            self.clien  = MongoClient(mongoUrl)
            self.db     = self.clien[self.dbasM]             
            return self.db
        except errors.ServerSelectionTimeoutError as err:
            print(f'Error Exception: {str(err)}')
            raise
        except Exception as e:
            print(f'Error Exception: {str(e)}')
            raise
        
    def setCloseConexion(self):
        if self.clien:
            self.clien.close()