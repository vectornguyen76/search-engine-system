import uuid
from app.db import Base
from sqlalchemy import Column, String
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    def __init__(self, username, password):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = self.get_password_hash(password)
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        
        return pwd_context.hash(password)