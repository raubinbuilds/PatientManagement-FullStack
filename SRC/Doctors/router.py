from fastapi import APIRouter,Depends,status,HTTPException,Request
from sqlalchemy.orm import Session
from SRC.utils.db import get_db
from SRC.Doctors.dtos import DrSchema,DrResponseSchema,DrLogin
from SRC.Doctors import controller
from SRC.utils.helpers import is_authenticated
from SRC.Doctors.models import Doctor
Dr_routes=APIRouter(prefix='/Doctor')
@Dr_routes.post("/register",response_model=DrResponseSchema,status_code=status.HTTP_201_CREATED)
def register(body:DrSchema,db:Session=Depends(get_db)):
    return controller.register(body,db)
@Dr_routes.post("/login",status_code=status.HTTP_200_OK)
def login(body:DrLogin,db:Session=Depends(get_db)):
    return controller.login(body,db)
@Dr_routes.put("/update",status_code=status.HTTP_200_OK)
def update(Body:DrResponseSchema,db:Session=Depends(get_db),doctor:Doctor=Depends(is_authenticated)):
    return controller.update(Body,doctor,db)
@Dr_routes.get("/is_auth",response_model=DrResponseSchema,status_code=status.HTTP_200_OK)
def isAuthenticated(request:Request,db:Session=Depends(get_db)):
    return isAuthenticated(request,db)