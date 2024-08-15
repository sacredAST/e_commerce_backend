from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.marketplace import Marketplace
from app.database import get_db
from app.schemas.marketplace import MarketplaceCreate, MarketplaceUpdate, MarketplaceRead
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging
from pydantic import ValidationError

async def create_marketplace(db: AsyncSession, marketplace: MarketplaceCreate):
    db_marketplace = Marketplace(**marketplace.dict())
    db.add(db_marketplace)
    await db.commit()
    await db.refresh(db_marketplace)
    return {"msg": "success"}

async def get_marketplace(db: AsyncSession, marketplace_id: int):
    result = await db.execute(select(Marketplace).filter(Marketplace.id == marketplace_id))
    return result.scalars().first()

async def get_marketplaces(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Marketplace).offset(skip).limit(limit))
    return result.scalars().all()

async def update_marketplace(db: AsyncSession, marketplace_id: int, marketplace: MarketplaceUpdate):
    db_marketplace = await get_marketplace(db, marketplace_id)
    if db_marketplace is None:
        return None
    for key, value in marketplace.dict().items():
        setattr(db_marketplace, key, value)
    await db.commit()
    await db.refresh(db_marketplace)
    return db_marketplace

async def delete_marketplace(db: AsyncSession, marketplace_id: int):
    db_marketplace = await get_marketplace(db, marketplace_id)
    if db_marketplace is None:
        return None
    await db.delete(db_marketplace)
    await db.commit()
    return db_marketplace

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_marketplace(marketplace: MarketplaceCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_marketplace(db, marketplace)
    except ValidationError as e:
        logging.error(f"Validation error: {e.errors()}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
    except Exception as e:
        logging.error(f"Error creating marketplace: {e}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@router.get("/{marketplace_id}", response_model=MarketplaceRead)
async def read_marketplace(marketplace_id: int, db: AsyncSession = Depends(get_db)):
    marketplace = await get_marketplace(db, marketplace_id)
    if marketplace is None:
        raise HTTPException(status_code=404, detail="Marketplace not found")
    return marketplace

@router.get("/", response_model=List[MarketplaceRead])
async def read_marketplaces(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_marketplaces(db, skip=skip, limit=limit)

@router.put("/{marketplace_id}", response_model=MarketplaceRead)
async def update_existing_marketplace(marketplace_id: int, marketplace: MarketplaceUpdate, db: AsyncSession = Depends(get_db)):
    updated_marketplace = await update_marketplace(db, marketplace_id, marketplace)
    if updated_marketplace is None:
        raise HTTPException(status_code=404, detail="Marketplace not found")
    return updated_marketplace

@router.delete("/{marketplace_id}")
async def delete_existing_marketplace(marketplace_id: int, db: AsyncSession = Depends(get_db)):
    deleted_marketplace = await delete_marketplace(db, marketplace_id)
    if deleted_marketplace is None:
        raise HTTPException(status_code=404, detail="Marketplace not found")
    return {"msg": "success"}