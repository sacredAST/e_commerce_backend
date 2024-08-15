from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Dict
from typing import Optional

class Credentials(BaseModel):
    type: Optional[str] = None
    firstKey: Optional[str] = None
    secondKey: Optional[str] = None

class CRUDOperations(BaseModel):
    endpoint: Optional[str] = None
    create: Optional[str] = None
    read: Optional[str] = None
    update: Optional[str] = None
    delete: Optional[str] = None
    count: Optional[str] = None

class MarketplaceBase(BaseModel):
    image_url: Optional[str] = None
    title: Optional[str] = None
    owner: Optional[str] = None
    baseURL: Optional[str] = None
    marketplaceDomain: Optional[str] = None
    country: Optional[str] = None
    baseAPIURL: Optional[str] = None
    credentials: Optional[Credentials] = None
    products_crud: Optional[CRUDOperations] = None
    orders_crud: Optional[CRUDOperations] = None

class MarketplaceCreate(MarketplaceBase):
    pass

class MarketplaceUpdate(MarketplaceBase):
    pass

class MarketplaceRead(MarketplaceBase):
    id: int

    class Config:
        orm_mode = True
