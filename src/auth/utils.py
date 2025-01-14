from passlib.context import CryptContext
from src.config import Config
from datetime import datetime, timedelta
import jwt
import uuid
import logging

ACCESS_TOKEN_EXPIRE_MINUTES = 60
passwd_context = CryptContext(schemes=["bcrypt"])

def generate_password_hash(password: str) -> str:
    return passwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return passwd_context.verify(password, hashed_password)


def create_access_token(user_data: dict, 
                        expiry: timedelta = None, 
                        refresh: bool = False):
    payload = {}
    
    payload['user'] = user_data
    payload['exp'] = datetime.now() + expiry if expiry is not None else datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["jti"] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
        