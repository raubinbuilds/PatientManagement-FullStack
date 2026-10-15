from sqlalchemy import Column,INTEGER,DateTime,Boolean,String,ForeignKey,Date,Time
from SRC.utils.db import Base
from datetime import datetime,timezone
class Appointment(Base):
    __tablename__ = "appointment_table"

    appointment_id = Column(INTEGER, primary_key=True, index=True)
    doctor_id = Column(String, ForeignKey("dr_table.dr_id"))
    patient_id = Column(String, ForeignKey("patient_table.patient_id"))
    appointment_date = Column(Date)
    appointment_time = Column(Time)
    reason = Column(String)
    status = Column(String, default="booked")
    created_at = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))