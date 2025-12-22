from datetime import timedelta, datetime
from jose import JWTError, jwt
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 60

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes = ACCESS_TOKEN_EXPIRY_MINUTES))
    to_encode.update({"exp":expire})
    return(jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM))

def decode_access_token(token: "str"):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithm = ALGORITHM)
        return(payload)   
    
    except JWTError:
        return None 
    