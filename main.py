from fastapi import FastAPI
from SRC.utils.db import Base,engine
from SRC.Doctors.router import Dr_routes
from SRC.Patients.router import patient_routes
from SRC.Appointment.router import App_routes
from SRC.OTP.router import auth_routes
Base.metadata.create_all(engine)
app=FastAPI(title="Patient MANAGEMENT APP")
app.include_router(Dr_routes)
app.include_router(patient_routes)
app.include_router(App_routes)
app.include_router(auth_routes)