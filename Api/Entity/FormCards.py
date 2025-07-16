from pydantic import BaseModel
from datetime import datetime

class FormCards(BaseModel):
    
    idUser: str    
    cardName: str
    cardType: int
    cardFIni: int
    cardFEnd: int
    cardFPay: int
