from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db import SessionLocal
from src.models import UserModel
from src.schemas.user_schema import CreateUserSchema, ResponeUserSchema
from src.utils import LOGGER

router = APIRouter(
    prefix="", tags=["user"], responses={404: {"description": "Not found"}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/hello")
async def get_hello():
    LOGGER.info("hello")
    return "Hello"


@router.get("/get-user-all", response_model=list[ResponeUserSchema])
async def get_user_all(db: Session = Depends(get_db)):
    user = db.query(UserModel).all()
    return user


@router.post("/register", response_model=ResponeUserSchema)
async def add_user(data_user: CreateUserSchema, db: Session = Depends(get_db)):
    try:
        new_user = UserModel(username=data_user.username, password=data_user.password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        LOGGER.info(f"Register Successfully! Username: {data_user.username}")
    except Exception as ex:
        LOGGER.error(f"Register Failed! Error: {ex}")

    return new_user


@router.get("/get-user")
async def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    return user
