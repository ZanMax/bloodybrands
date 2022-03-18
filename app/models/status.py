from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(String(100), unique=True, index=True)
