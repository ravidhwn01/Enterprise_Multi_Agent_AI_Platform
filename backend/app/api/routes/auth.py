


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

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    print("PASSWORD:", user.password)
    print("TYPE:", type(user.password))
    print("LENGTH:", len(user.password))

    # Hash password
    hashed_password = hash_password(user.password)
    print("HASHED PASSWORD:", hashed_password)

    # Create new user
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    # Save to database
    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


# =========================
# LOGIN USER
# =========================

@router.post(
    "/login",
    response_model=Token
)
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    # Find user by email
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    # User not found
    if not existing_user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Verify password
    is_valid = verify_password(
        user.password,
        existing_user.hashed_password
    )

    # Password incorrect
    if not is_valid:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": existing_user.email
        }
    )

    # Return token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }