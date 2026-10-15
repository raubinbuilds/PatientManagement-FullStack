from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from SRC.utils.db import get_db
from SRC.utils import settings
from SRC.Patients.models import UserModel as PatientModel
from SRC.Doctors.models import UserModel as DoctorModel
from datetime import datetime,timezone
import jwt
from jwt.exceptions import InvalidTokenError


def is_authenticated(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        token = request.headers.get("authorization")

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization token missing"
            )

        token = token.split(" ")[-1]

        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = data.get("id")
        role = data.get("role")
        exp_time = data.get("exp")

        if not user_id or not role or not exp_time:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        if datetime.now(timezone.utc).timestamp() >= exp_time:
            raise HTTPException(
                status_code=401,
                detail="Token expired"
            )

        if role == "patient":
            user = db.query(PatientModel).filter(
                PatientModel.patient_id == user_id
            ).first()

        elif role == "doctor":
            user = db.query(DoctorModel).filter(
                DoctorModel.dr_id == user_id
            ).first()

        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid user role"
            )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )