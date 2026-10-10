from SRC.Patients.dtos import PatientResponseSchema,patientSchema,LoginSchema
from SRC.Patients.models import Patient
from SRC.utils.db import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request
from pwdlib import PasswordHash
from SRC.utils.settings import settings
from datetime import datetime, timedelta
import jwt

from jwt.exceptions import InvalidTokenError

password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def register(Body: patientSchema, db: Session):
    is_user = db.query(Patient).filter(Patient.username == Body.username).first()
    if is_user:
        raise HTTPException(409, "User already exists")

    is_user = db.query(Patient).filter(Patient.email == Body.email).first()
    if is_user:
        raise HTTPException(409, "Email already logged in")

    hash_password = get_password_hash(Body.password)
    new_user = Patient(
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
    return new_user


def login(Body:LoginSchema, db: Session):
    is_user = db.query(Patient).filter(Patient.username == Body.username).first()
    if not is_user:
        raise HTTPException(401, "User not found")

    
    if not verify_password(Body.password, is_user.hash_password):
        raise HTTPException(401, "wrong password")

    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    token = jwt.encode(
        {"_id": is_user.id, "exp": exp_time},
        settings.SECRET_KEY,
        settings.ALGORITHM
    )
    return {"token": token}



def update(Body:LoginSchema, db: Session):
    is_user = db.query(Patient).filter(
        Patient.username == Body.username
    ).first()

    if not is_user:
        raise HTTPException(404, "User not found")

    if not verify_password(Body.password, is_user.hash_password):
        raise HTTPException(401, "Wrong password")

    is_user.name = Body.name
    is_user.Specialist = Body.Specialist
    is_user.email = Body.email
    is_user.mobile = Body.mobile

    db.commit()
    db.refresh(is_user)

    return is_user



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

        user_id = data.get("_id")

        if user_id is None:
            raise HTTPException(401, "Invalid token")

        user = db.query(Patient).filter(
            Patient.id == user_id
        ).first()

        if not user:
            raise HTTPException(401, "User not found")

        return user

    except InvalidTokenError:
        raise HTTPException(401, "You are unauthorised")