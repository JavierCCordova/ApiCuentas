from pydantic import BaseModel

class User(BaseModel):

    usuario:  str
    password: str