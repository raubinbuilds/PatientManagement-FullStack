from sqlalchemy import Column,INTEGER,DateTime,Boolean,String,ClauseList
from SRC.utils.db import Base
class Doctor(Base):
    __tablename__="dr_table"
    id=Column(INTEGER,primary_key=True)
    name=Column(String)
    username=Column(String,nullable=False)
    Specialist=Column(String,nullable=False)
    hash_password=Column(String,nullable=False)
    email=Column(String,nullable=False)
    mobile=Column(String ,nullable=False)

