from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.db.database import Base


class File(Base):
    """
    Database model for uploaded files.
    """

    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String,nullable=False)
    stored_filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  
    file_path = Column(String, nullable=False)

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id")
    )