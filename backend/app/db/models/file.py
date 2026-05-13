from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.db.database import Base


class File(Base):

    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    filepath = Column(String)

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id")
    )