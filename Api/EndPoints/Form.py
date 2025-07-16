from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse

from Api.Db.Conexion import Conexion
from Api.Model.ModelForm import ModelForm
from Api.Entity.UserID import UserId
from Api.Entity.FormConsumption import formConsumption
from Api.Entity.FormCards import FormCards
from Api.Entity.FormEstablishment import FormEstablishment
from Api.Entity.FormIncome import FormIncome

Conn    = Conexion()
FormMod = ModelForm()

routerF = APIRouter(
    prefix= '/Form',
    tags= ['Form']
)

@routerF.post("/GetForm")
async def getForm(form:UserId):
    db               =  Conn.getConexion()
    status, response =  FormMod.getFormlist(db=db,form=form) 
    return JSONResponse(status_code=status,content=response)


@routerF.post("/SetFormConsumption")
async def setForm(form:formConsumption):
    db              =   Conn.getConexion()
    response        =   FormMod.setFormConsumption(db,form)
    return JSONResponse( status_code= response['status'],content = response)

@routerF.post("/SetFormCards")
async def setFormCard(card:FormCards):
    db          =   Conn.getConexion()
    response    =   FormMod.setFormCard(db=db,card=card)
    return JSONResponse(status_code=response['status'],content=response)

@routerF.post("/SetEstablishment")
async def setEstablisment(est:FormEstablishment):
    db          =   Conn.getConexion()
    response    =   FormMod.setFormEstablishment(db,est)
    return JSONResponse(status_code=response['status'],content=response )

@routerF.post("/SetIncome")
async def setIncome(income:FormIncome):
    db          =   Conn.getConexion()
    response    =   FormMod.setInconme(db,income)
    return JSONResponse(status_code=response['status'],content=response )

 