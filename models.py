from email.policy import default
from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class signup(Base):
    __tablename__ = "signup"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    contact = Column(String(100))
    password = Column(String(100))
