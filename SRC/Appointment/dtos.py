from pydantic import BaseModel
from datetime import date,time,datetime
class AppointmentSchema:
     appointment_date:date
     appointment_time:time
     reason:str
     status:str="Booked"
     created_at:datetime
class ResponseAppointmentSchema:
     appointment_date:date
     appointment_time:time