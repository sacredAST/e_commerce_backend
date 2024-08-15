from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db

router = APIRouter()

@router.get('/dashboard')
async def get_dashboard_info(db: AsyncSession = Depends(get_db)):
    return ''