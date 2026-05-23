
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.user import User

from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    UserResponse
)

from app.schemas.token_schema import Token

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.curd.user import get_user_by_email, create_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================
# REGISTER USER
# =========================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    # # Check if email already exists
    # existing_user = db.query(User).filter(
    #     User.email == user.email
    # ).first()
    
    existing_user = get_user_by_email(db, user.email)

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        


    # Hash password
    hashed_password = hash_password(user.password)

    # # Create new user
    # new_user = User(
    #     username=user.username,
    #     email=user.email,
    #     hashed_password=hashed_password
    
    # )
    hashed_password = hash_password(
    user.password
)

    # new_user = create_user(
    #     db=db,
    #     username=user.username,
    #     email=user.email,
    #     hashed_password=hashed_password
    # )
    new_user = create_user(db,user)

    # Save to database
    # db.add(new_user)

    # db.commit()

    # db.refresh(new_user)

    return new_user


# =========================
# LOGIN USER
# =========================

@router.post(
    "/login",
    response_model=Token
)
@router.post("/login")
def login_user(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)

):

    existing_user = get_user_by_email(
        db,
        form_data.username
    )

    if not existing_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    is_valid = verify_password(
        form_data.password,
        existing_user.hashed_password
    )

    if not is_valid:

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = create_access_token(
        data={
            "sub": existing_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    