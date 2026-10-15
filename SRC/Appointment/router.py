from fastapi import APIRouter,Depends,status,HTTPException,Request
from utils.db import get_db
from sqlalchemy.orm import Session
from SRC.Appointment import controller 
from SRC.Appointment.dtos import AppointmentSchema,ResponseAppointmentSchema
from SRC.Patients.models import Patient
from SRC.Doctors.models import Doctor
from SRC.Patients.dtos import LoginSchema
from SRC.Doctors.dtos import DrLogin
from SRC.Appointment.models import Appointment
from SRC.utils.helpers import is_authenticated
App_routes=APIRouter(prefix="/appointment")
@App_routes.post("/bookAppointment/",status_code=status.HTTP_201_CREATED)
def bookAppointment(body:AppointmentSchema,P:Patient=Depends(is_authenticated),db:Session=Depends(get_db)):
 return controller.bookAppointment(P,body,db);
@App_routes.get("/Getappointments/{appointment_id}")
def getAppointmentDetails(appointment_id:int,db:Session=Depends(get_db)):
    return controller.getAppointmentDetails(appointment_id,db);
@App_routes.get("/doctors/{dr_id}/appointments",status_code=status.HTTP_200_OK)
def getAppointmentDetails_DR(dr_id:str,db:Session=Depends(get_db),DR:Doctor=Depends(is_authenticated)):
    return controller.getAppointmentDetails_DR(dr_id,db,DR);
@App_routes.get("/patients/{patient_id}/appointments",status_code=status.HTTP_200_OK)
def getAppointmentDetails_Patient(patient_id:str,db:Session=Depends(get_db),P:Patient=Depends(is_authenticated)):
    return controller.getAppointmentDetails_Patient(patient_id,db,P);
@App_routes.put("/ChangeDateTime/{appointment_id}",status_code=status.HTTP_200_OK)
def ChangeDateTime(body:ResponseAppointmentSchema,appointment_id:int,db:Session=Depends(get_db),DR:Doctor=Depends(is_authenticated)):
    return controller.ChangeDateTime(body,appointment_id,db,DR);
@App_routes.delete("/appointments/{appointment_id}",status_code=status.HTTP_200_NO_CONTENT)
def CancelAppointment(appointment_id:int,db:Session=Depends(get_db),P:Patient=Depends(is_authenticated)):
    return controller.CancelAppointment(appointment_id,db,P);