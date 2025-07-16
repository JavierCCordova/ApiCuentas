from fastapi import routing,APIRouter
from fastapi.responses import JSONResponse
from Api.Entity.UserID import UserId
from Api.Entity.IdConsumption import IdConsuption
from Api.Model.ModelConsumption import ModelConsumption
from Api.Db.Conexion import Conexion

rounterCon =  APIRouter(
    prefix='/Consum',
    tags = ["Consump"]
)

conn    = Conexion()
consump = ModelConsumption() 


@rounterCon.post("/Consumption")
async def getConsumption(consumo: UserId):
    db          =   conn.getConexion()
    response    =   consump.getConsumptionmonth(consumo,db) 
    return JSONResponse(status_code=response['status'],content=response)

@rounterCon.delete('/ConsumptionDelete')
async def setConsumptionDelete(idconsumption:IdConsuption):
    if len(idconsumption.idConsumption) != 24:
        return JSONResponse(status_code=401,content={'status':401,'detail':'Id No tiene la longitud'})
    db          =   conn.getConexion()
    response    =   consump.setConsumptionDelete(idconsumption,db)
    return JSONResponse(status_code=response['status'],content=response)