from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from Api.Db.Conexion import Conexion
from Api.Model.ModelDetail import ModelDetail
from Api.Entity.UserID import UserId

routingDetail = APIRouter(
    prefix='/Detail',
    tags=['Detail']
)
conn        =   Conexion()
detail      =   ModelDetail()

@routingDetail.post('/getDetaildata')
async def getDetailData(idUser:UserId):    
    db          =   conn.getConexion()
    response    =   detail.getDetailData(idUser,db)
    return JSONResponse(status_code=response['status'],content=response)