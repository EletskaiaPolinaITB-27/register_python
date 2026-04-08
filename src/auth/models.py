from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

from src.database import Base




class User(Base):
    __tablename__ = "users"



    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    password = Column(String, nullable=False)
    products = relationship("Product" , back_populates="user")