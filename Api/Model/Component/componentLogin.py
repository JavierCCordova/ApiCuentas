from pymongo.errors import PyMongoError
import traceback

def getValidateUser(user,db):
    try:
        datos  = dict(status = 0,usuario="", perfil=0)
        status = 200 
        
        collection  =   db['llamaUser'] # collection
        result      =   collection.find_one({"userName": user.usuario, "userPass": user.password})
        if result:
            datos['status']  = status
            datos['usuario'] = result['userFull']
            datos['perfil']  = result['userProfile']
            datos['id']      = str(result['_id'])
            return 1,datos,status
        else:
            datos['status']  = 401
            return 0,datos,401
        
    except ConnectionError as e:
        print(f"Errore de DDBB: {str(traceback.format_exc())}")
        return -1,{'status':500,'Error': f"Errore de inesperado: {str(traceback.format_exc())}"},500
    except PyMongoError as e:
        print(f"Errore de Pymongo: {str(traceback.format_exc())}")
        return -2,{'status':500,'Error': f"Errore de inesperado: {str(traceback.format_exc())}"},500
    except Exception as e:
        print(f"Errore de inesperado: {str(traceback.format_exc())}")
        return -3,{'status':500,'Error': f"Errore de inesperado: {str(traceback.format_exc())}"},500