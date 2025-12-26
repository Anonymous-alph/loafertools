from pydantic import BaseModel, EmailStr

# Request/Response schemas
class UserRegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    message: str
