from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from SRC.OTP import controller
from SRC.utils.db import get_db
from SRC.OTP.dtos import verify,send
from SRC.OTP import controller
purpose1="patient-register"
purpose2="doctor-register"
auth_routes=APIRouter(prefix="/Auth")
@auth_routes.post("/patients/send-otp",status_code=status.HTTP_200_OK)
def create_otp(body:send,purpose1:str,db:Session=Depends(get_db)):
    return controller.create_otp(body,purpose1,db)
@auth_routes.post("/doctors/send-otp",status_code=status.HTTP_200_OK)
def create_otp(body:send,purpose2:str,db:Session=Depends(get_db)):
    return controller.status(body,purpose2,db)
@auth_routes.post("/patients/verify-otp",status_code=status.HTTP_202_ACCEPTED)
def authPatient(body:verify,db:Session=Depends(get_db)):
    return controller.authPatient(body,db)
@auth_routes.post("/doctors/verify-otp",status_code=status.HTTP_202_ACCEPTED)
def authDoctor(body:verify,db:Session=Depends(get_db)):
    return controller.authDoctor(body,db)
