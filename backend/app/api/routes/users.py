from fastapi import APIRouter, Depends, HTTPException, status 

from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.user_schema import  UserUpdate, UserResponse, UserDelete
from app.api.dependencies import get_current_user

from app.curd.user import (
    get_user_by_id,
    update_user,
    delete_user,
    delete_user_by_email,
    get_all_users
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/me",
    response_model=UserResponse
)
def get_logged_in_user(
    current_user: User = Depends(get_current_user)
):
    print({"message": "This endpoint will return the logged-in user's information.", "user": current_user})
    return current_user
    # return {"message": "This endpoint will return the logged-in user's information."}




# DELETE USER BY ID

@router.delete("/delete/id/{user_id}")
def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = get_user_by_id(
        db,
        user_id
    )
    print({"message": "Attempting to delete user by ID", "user_id": user_id, "user_found": user is not None})

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    delete_user(
        db,
        user
    )

    return {
        "message": f"User with ID {user_id} deleted successfully"
    }


# DELETE USER BY EMAIL

@router.delete("/delete/email/{email}")
def delete_user_by_email(
    email: str,
    db: Session = Depends(get_db)
):

    user = delete_user_by_email(
        db,
        email
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    delete_user(
        db,
        user
    )

    return {
        "message": f"User with email {email} deleted successfully"
    }





#  update the user info.
@router.put("/update/{user_id}", response_model=UserResponse)
def update_user_info(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)   
):
    user = update_user(
        db,
        user_id,
        user_update
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user



@router.get(
    "/all",
    response_model=list[UserResponse]
)
def get_all_user(
    db: Session = Depends(get_db)
):
    return get_all_users(db)