from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    company = Column(String, index=True)
    phone = Column(String, index=True)
    country = Column(String, index=True)
    avatar = Column(String, nullable=True)

    user = relationship("User", back_populates="profile")