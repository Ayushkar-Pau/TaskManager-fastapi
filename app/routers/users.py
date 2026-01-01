from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# --Custom import
from app.models import UserResponse
from app.database import get_db
from app.db_models import DBUser
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


# --read_users--
@router.get("/secretcode", response_model=list[UserResponse], include_in_schema=True)
def read_users(
    db: Session = Depends(get_db),
    current_user: OAuth2PasswordRequestForm = Depends(get_current_user),
):
    if current_user.email != "ayuayu11@gmail.com":
        raise HTTPException(status_code=403, detail="Access Denied!")

    return db.query(DBUser).all()

