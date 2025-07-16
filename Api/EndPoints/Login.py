from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from Api.Entity.User import User
from Api.Model.ModelLogin import ModelLogin
from Api.Db.Conexion import Conexion

LogMod  = ModelLogin()
Conn    = Conexion() 

router  = APIRouter(
    prefix='/Login',
    tags=["Items"]
)

@router.post("/Inicio")
async def Inicio(user:User):
    db              =   Conn.getConexion()
    Response,status =   LogMod.getValidateUser(user,db)
    return JSONResponse(status_code=status,content=Response)