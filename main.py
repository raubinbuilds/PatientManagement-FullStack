from fastapi import FastAPI
from SRC.utils.db import Base,engine
from SRC.Doctors.router import Dr_routes
from SRC.Patients.router import patient_routes
Base.metadata.create_all(engine)
app=FastAPI(title="Patient MANAGEMENT APP")
app.include_router(Dr_routes)
app.include_router(patient_routes)