from fastapi import APIRouter,Depends,status,HTTPException,Request
from SRC.Patients.dtos import patientSchema,PatientResponseSchema, LoginSchema
from SRC.utils.db import get_db
from SRC.Patients import controller
from sqlalchemy.orm import session
patient_routes=APIRouter(prefix='/patient')
@patient_routes.post("/register",response_model=PatientResponseSchema,status_code=status.HTTP_201_CREATED)
def register(body:patientSchema,db:session=Depends(get_db)):
    return controller.register(body,db)
@patient_routes.post("/login",status_code=status.HTTP_200_OK)
def login(body:LoginSchema,db:session=Depends(get_db)):
    return controller.login(body,db)
@patient_routes.put("/update",status_code=status.HTTP_200_OK)
def update(body:patientSchema,db:session=Depends(get_db)):
    return controller.update(body,db)
@patient_routes.get("/is_auth",response_model=PatientResponseSchema,status_code=status.HTTP_200_OK)
def is_auth(request:Request,db:session=Depends(get_db)):
    return controller.is_authenticated(request,db)