from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True)
