from fastapi import APIRouter,HTTPException,Depends
from fastapi.responses import JSONResponse
from Api.Entity.UserID import UserId
from Api.Db.Conexion import Conexion
from Api.Model.ModelDash import ModelDash

routerDas = APIRouter(
    prefix = '/Dash',
    tags   = ['Dash']
)

Conn = Conexion()
Dash = ModelDash()


@routerDas.post('/getInformation')
async def getInformation(userId: UserId):
    db          =   Conn.getConexion()
    response    =   Dash.GetDataConsumption(userId,db)
    return JSONResponse(status_code=response['status'],content= response)
