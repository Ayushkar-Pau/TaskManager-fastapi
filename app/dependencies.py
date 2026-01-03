from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
import jwt
from fastapi.security import OAuth2PasswordBearer


from app.db_models import DBUser
from app.database import get_db

load_dotenv()


# This tells FastAPI: "Look for a Bearer token in the Authorization header"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 1. Decode the 'Wristband' (Token)
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
        )
        email: str = payload.get("sub")
        user_scopes: list = payload.get("scopes", [])

        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    # 2. Look for the user in the Database
    user = db.query(DBUser).filter(DBUser.email == email).first()
    if user is None:
        raise credentials_exception

    user.current_scopes = user_scopes
    # 3. If everything is good, return the user object
    return user
