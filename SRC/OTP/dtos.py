from pydantic import BaseModel,EmailStr,Field
class verify(BaseModel):
    email:EmailStr
    otp: str = Field(pattern=r"^\d{6}$")
class send(BaseModel):
    email:EmailStr
    