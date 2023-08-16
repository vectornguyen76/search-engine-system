from pydantic import BaseModel

class CreateUserSchema(BaseModel):
    username: str
    password: str

class ResponeUserSchema(BaseModel):
    id: str
    username: str