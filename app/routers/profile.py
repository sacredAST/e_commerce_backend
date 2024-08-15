from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileRead
from app.database import get_db
from app.routers.auth import get_current_user
from app.models.user import User
from app.models.profile import Profile

router = APIRouter()

async def get_profile(db: AsyncSession, user_id: int):
    result = await db.execute(select(Profile).filter(Profile.user_id == user_id))
    return result.scalars().first()

async def create_profile(db: AsyncSession, profile: ProfileCreate, user_id: int):
    db_profile = Profile(**profile.dict(), user_id=user_id)
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)
    return db_profile

async def update_profile(db: AsyncSession, profile: ProfileUpdate, user_id: int):
    db_profile = await get_profile(db, user_id)
    if db_profile:
        for key, value in profile.dict(exclude_unset=True).items():
            setattr(db_profile, key, value)
        await db.commit()
        await db.refresh(db_profile)
    return db_profile

@router.get("/profile", response_model=ProfileRead)
async def read_profile(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    profile = await get_profile(db, user_id=current_user.id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/profile", response_model=ProfileRead)
async def create_profile(profile: ProfileCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_profile = await get_profile(db, user_id=current_user.id)
    if db_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")
    return await create_profile(db, profile, user_id=current_user.id)

@router.put("/profile", response_model=ProfileRead)
async def update_profile(profile: ProfileUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await update_profile(db, profile, user_id=current_user.id)
