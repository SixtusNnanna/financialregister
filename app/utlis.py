import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

load_dotenv()
secrets = os.getenv("SECRETS")
access_token_exp_time = 30
algorithm = os.getenv("ALGORITHM")


def create_access_token(payload: dict, expiry: timedelta | None = None):
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + \
        (expiry or timedelta(minutes=access_token_exp_time))
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, key=secrets, algorithm=algorithm
    )

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token=token, key=secrets,
            algorithms=[algorithm]
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expires access token")





