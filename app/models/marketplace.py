from sqlalchemy import Column, Integer, String, JSON
from app.database import Base

class Marketplace(Base):
    __tablename__ = 'marketplaces'

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    baseURL = Column(String, nullable=False)
    marketplaceDomain = Column(String, nullable=False)
    country = Column(String, nullable=False)
    baseAPIURL = Column(String, nullable=False)
    credentials = Column(JSON, nullable=False)
    products_crud = Column(JSON, nullable=False)
    orders_crud = Column(JSON, nullable=False)
