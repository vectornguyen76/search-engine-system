
from fastapi import APIRouter, Depends, FastAPI, Request
from sqlalchemy.orm import Session
from app.models import UserModel
from app.db import SessionLocal
from app.schemas.user_schema import CreateUserSchema, ResponeUserSchema
import logging

# Create logger for this module
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        

@router.get("/hello")
async def get_hello():
    logger.info("hello")
    return "Hello"

@router.get("/get-user-all", response_model=list[ResponeUserSchema])
async def get_user(db: Session = Depends(get_db)):
    user = db.query(UserModel).all()
    return user

@router.post("/register", response_model=ResponeUserSchema)
async def add_user(data_user: CreateUserSchema, db: Session = Depends(get_db)):
    try:
        new_user = UserModel(username=data_user.username, password=data_user.password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"Register Successfully! Username: {data_user.username}")
    except:
        logger.error(f"Register Failed!")

    return new_user
    
@router.get("/get-user")
async def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    return user

import asyncio
async def fetch_data_from_database():
    print("ok")
    
    await asyncio.sleep(3)  # Simulate asynchronous database operation
    return "Data from the database"

@router.get("/get_data")
async def get_data():
    data = await fetch_data_from_database()
    print("ok")
    return {"data": data}