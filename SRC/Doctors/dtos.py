from pydantic import BaseModel
class DrSchema(BaseModel):
    name:str
    username:str
    password:str
    Specialist:str
    email:str
    mobile:str
class DrResponseSchema(BaseModel):
    username:str
    name:str
    id:int
    email:str
    mobile:str
class DrLogin(BaseModel):
    username:str
    password:str