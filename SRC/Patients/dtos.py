from pydantic import BaseModel
from typing import List
class patientSchema(BaseModel):
    name:str
    username:str
    password:str
    disease:list[str]
    email:str
    mobile:str
class PatientResponseSchema(BaseModel):
    name:str
    username:str
    password:str
    email:str
    mobile:str
class LoginSchema(BaseModel):
    username:str
    password:str
