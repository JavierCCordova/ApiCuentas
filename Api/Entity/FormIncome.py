from pydantic import BaseModel
from datetime import datetime

class FormIncome(BaseModel):

    idUser: str
    incAmount: float
    incDateI: datetime
    incDateF: datetime
    incAmountC: float = 1