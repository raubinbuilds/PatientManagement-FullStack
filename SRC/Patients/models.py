from sqlalchemy import Column,INTEGER,DateTime,Boolean,String
from sqlalchemy.dialects.postgresql import ARRAY
from SRC.utils.db import Base
class Patient(Base):
    __tablename__="patient_table"
    id=Column(INTEGER,primary_key=True)
    name=Column(String)
    username=Column(String,nullable=False)
    disease=Column(ARRAY(String),nullable=False)
    hash_password=Column(String,nullable=False)
    email=Column(String,nullable=False)
    mobile=Column(String ,nullable=False)

