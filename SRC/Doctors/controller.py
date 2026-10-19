from SRC.Doctors.dtos import DrResponseSchema, DrLogin, DrSchema
from SRC.Doctors.models import Doctor
from SRC.utils.db import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request
from pwdlib import PasswordHash
from SRC.utils.settings import settings
from datetime import datetime, timedelta,timezone
import jwt
from SRC.utils.mailservice import send_email
from jwt.exceptions import InvalidTokenError
from SRC.OTP.models import OTP
password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def register(Body: DrSchema, db: Session):
    otp_record=db.query(OTP).filter(OTP.email==Body.email,OTP.purpose=="doctor-register").first()
    if (not otp_record or not otp_record.is_verified or datetime.now(timezone.utc) > otp_record.expires_at):
        raise HTTPException(status_code=400,detail="You are not verified.Verify your email first")
    
    is_user = db.query(Doctor).filter(Doctor.username == Body.username).first()
    if is_user:
        raise HTTPException(409, "User already exists")

    is_user = db.query(Doctor).filter(Doctor.email == Body.email).first()
    if is_user:
        raise HTTPException(409, "Email already logged in")
    db.delete(otp_record)
    db.commit()

    hash_password = get_password_hash(Body.password)
    new_user = Doctor(
        name=Body.name,
        username=Body.username,
        Specialist=Body.Specialist,
        hash_password=hash_password,
        email=Body.email,
        mobile=Body.mobile
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    send_email(
        to_email=new_user.email,
        subject="Doctor registration successfull",
        body=f"Hello {new_user.name},your registration was successfull"
    )
    return new_user

def login(Body: DrLogin, db: Session):
    is_user = db.query(Doctor).filter(Doctor.username == Body.username).first()
    if not is_user:
        raise HTTPException(401, "User not found")

    
    if not verify_password(Body.password, is_user.hash_password):
        raise HTTPException(401, "wrong password")

    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    token = jwt.encode(
        {"id": is_user.dr_id, "exp": exp_time,"role":"doctor"},
        settings.SECRET_KEY,
        settings.ALGORITHM
    )
    return {"token": token}



def update(Body: DrResponseSchema, doctor:Doctor,db:Session):
    

    doctor.name = Body.name
    doctor.Specialist = Body.Specialist
    doctor.email = Body.email
    doctor.mobile = Body.mobile

    db.commit()
    db.refresh(doctor)

    return  {"message": "Doctor details updated successfully"}



def isAuthenticated(request: Request, db: Session):
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(401, "You are unauthorised")

        token = auth_header.split(" ", 1)[1]

        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = data.get("id")

        if user_id is None:
            raise HTTPException(401, "Invalid token")

        user = db.query(Doctor).filter(
            Doctor.dr_id == user_id
        ).first()

        if not user:
            raise HTTPException(401, "User not found")

        return user

    except InvalidTokenError:
        raise HTTPException(401, "You are unauthorised")