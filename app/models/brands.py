from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Brands(Base):
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True)
    status_id = Column(Integer, ForeignKey('status.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    status = relationship("Status")
    category = relationship("Category")
