from SRC.utils.db import get_db
from SRC.OTP.models import OTP
import secrets
from fastapi import HTTPException,Depends,status
from sqlalchemy.orm import Session
from SRC.OTP.dtos import verify,send
from SRC.utils.mailservice import send_email
from pwdlib import PasswordHash
from datetime import datetime,timedelta,timezone

password_hash=PasswordHash.recommended()
def get_otp_hash(otp):
    return password_hash.hash(otp)
def verify_otp(otp,otp_hash):
    return password_hash.verify(otp,otp_hash)
def create_otp(body:send,purpose:str,db:Session):
    otp=f"{secrets.randbelow(1000000):06d}"
    otp_record=OTP(
        email = body.email,
        otp_hash = get_otp_hash(otp),
        purpose = purpose,
        expires_at = datetime.now(timezone.utc)+timedelta(minutes=5),
        is_verified = False
    )
    db.add(otp_record)
    db.commit()
    send_email(
        to_email=body.email,
        subject="One Time Password for registration",
        body=f"Here is your otp {otp},please enter correct otp"
    )
    return {"message":"OTP sent successfully"}
def authPatient(body:verify,db:Session):
    otp_record=db.query(OTP).filter(body.email==OTP.email,OTP.purpose == "patient-register").first()
    if not otp_record:
        raise HTTPException(status_code=404,detail="Enter correct email")
    if datetime.now(timezone.utc)>otp_record.expires_at:
        db.delete(otp_record)
        db.commit()
        raise HTTPException(status_code=400,detail="Time expired.Please request a new otp")
    if otp_record.is_verified:
         raise HTTPException(
            status_code=400,
            detail="OTP already verified"
              )
    if not verify_otp(body.otp,otp_record.otp_hash):
        raise HTTPException(status_code=404,detail="Invalid OTP")
    
    
    otp_record.is_verified=True
    db.commit()
    return {"message":"Email verified successfully"}
def authDoctor(body:verify,db:Session):
    otp_record=db.query(OTP).filter(body.email==OTP.email,OTP.purpose == "doctor-register").first()
    if not otp_record:
        raise HTTPException(status_code=404,detail="Enter correct email")
    if datetime.now(timezone.utc)>otp_record.expires_at:
            db.delete(otp_record)
            db.commit()
            raise HTTPException(status_code=400,detail="Time expired.Please request a new otp")
    if otp_record.is_verified:
             raise HTTPException(
                status_code=400,
                detail="OTP already verified"
                )
    if not verify_otp(body.otp,otp_record.otp_hash):
        raise HTTPException(status_code=404,detail="Invalid OTP")
    
    
    otp_record.is_verified=True
    db.commit()
    return {"message":"Email verified successfully"}
    