from  sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import hash_password


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
    
    
    
    
def  get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()




def create_user(
    db: Session,
    # username: str,
    # email: str,
    # hashed_password: str
    user : UserCreate
):
    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user



def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.password is not None:
        user.password = hash_password(user_update.password)
    db.commit()
    db.refresh(user)
    return user


def delete_user(
    db: Session,
    user: User
):

    db.delete(user)

    db.commit()


# delete by email
def delete_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user

def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def delete_all_users(db: Session):
    db.query(User).delete()
    db.commit()
    return True
    
