from pydantic import BaseModel
from bson import ObjectId

class formConsumption(BaseModel):

    idUser:str
    consDay: str
    consDiner : float
    consTyPay: str
    consProd: str
    consCard: str
    consCouta: int
 