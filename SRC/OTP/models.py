from sqlalchemy import Column, Integer, String, Boolean, DateTime
from SRC.utils.db import Base


class OTP(Base):
    __tablename__ = "otp_table"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    otp_hash = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)