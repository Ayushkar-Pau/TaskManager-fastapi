from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db_models import DBUser
from app.models import UserResponse, UserCreate
from app.database import get_db
from app.utils import hash_password, verify_password, create_access_token


router = APIRouter(tags=["Authentication"])


# --sign-up--
@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # if user already exists
    existing_user = db.query(DBUser).filter(DBUser.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # hash the pwd
    print(user_data.password)
    hashed_pwd = hash_password(user_data.password)

    # create the DB object
    new_user = DBUser(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd,
        role="user",
    )

    # save and return
    db.add(new_user)
    db.commit()

    return new_user


# --Login--
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(DBUser).filter(DBUser.email == form_data.username).first()

    # if user or pwd dont match
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    # 3. Create the 'JWT'
    token = create_access_token(data={"sub": user.email, "role": user.role})

    # 4. Return it to the user
    return {"access_token": token, "token_type": "bearer"}
