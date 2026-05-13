#create the text model here
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from app.db.database import Base


class Text(Base):
    __tablename__ = "texts"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(String)

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id")
    )
    