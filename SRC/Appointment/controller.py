from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from SRC.utils.db import get_db
from SRC.Patients.models import Patient
from SRC.Doctors.models import Doctor
from SRC.Appointment.dtos import AppointmentSchema,ResponseAppointmentSchema
from SRC.Appointment.models import Appointment

def bookAppointment(P:Patient,body:AppointmentSchema,db:Session):
    is_user=db.query(Patient).filter(Patient.patient_id==P.patient_id).first()
    if not is_user:
        raise HTTPException(status_code=404,detail="Not a valid user")
    
    new_user=Appointment(
        doctor_id =body.doctor_id,
        patient_id =body.patient_id,
        appointment_date =body.appointment_date,
        appointment_time =body.appointment_time,
        reason =body.reason,
        status = body.status,
        
        created_at = body.created_at
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
def getAppointmentDetails(appointment_id:int,db:Session):
    is_user=db.query(Appointment).filter(Appointment.appointment_id==appointment_id).first()
    if not is_user:
        raise HTTPException(status_code=404,detail="Appointment id doesn't exist")
    return is_user
def getAppointmentDetails_DR(dr_id:str,db:Session,DR:Doctor):
    is_user=db.query(Doctor).filter(Doctor.dr_id==DR.dr_id).first()
    if not is_user:
     raise HTTPException(status_code=404,detail="Not an authorised person")
    is_user=db.query(Appointment).filter(Appointment.doctor_id==dr_id)
    if not is_user:
        raise HTTPException(status_code=404,detail="No appointments")
    return is_user
def getAppointmentDetails_Patient(patient_id:str,db:Session,P:Patient):
    is_user=db.query(Patient).filter(Patient.patient_id==P.patient_id).first()
    if not is_user:
        raise HTTPException(status_code=404,detail="Not an authorised person")
    is_user=db.query(Appointment).filter(Appointment.patient_id==patient_id)
    if not is_user:
        raise HTTPException(status_code=404,detail="No appointments")
    return is_user
def ChangeDateTime(body:ResponseAppointmentSchema,appointment_id:int,db:Session,DR:Doctor):
    APD=db.query(Appointment).filter(Appointment.appointment_id==appointment_id).first()
    if not APD:
        raise HTTPException(status_code=404,detail="Appointment id doesn't exist")
    is_user=db.query(Appointment).filter(Appointment.doctor_id==DR.dr_id).first()
    if not is_user:
        raise HTTPException(status_code=404,detail="You are not an authorised person")
    APD.appointment_date=body.appointment_date
    APD.appointment_time=body.appointment_time
    db.commit()
    db.refresh(APD)
    return {"message":"Data and time for your Appointment has been updated"}
def CancelAppointment(appointment_id:int,db:Session,P:Patient):
    is_user=db.query(Patient).filter(Patient.patient_id==P.patient_id).first()
    if not is_user:
        raise HTTPException(status_code=404,detail="You are not an authorised person")
    appointment=db.query(Appointment).filter(Appointment.appointment_id==appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404,detail="Appointment ID doesn't exist")
    db.delete(appointment)
    db.commit()
    return {"message":"Appointment cancelled successfully"}