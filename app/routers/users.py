from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from pydantic import BaseModel
from typing import List
from app.database import get_db
from app.models.profile import Profile
from app.models.user import User
from app.routers.auth import Token, authenticate_user, update_last_logged_in
from app.schemas.profile import UserProfileRead, ProfileRead
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.schemas.response import UserResponse, ResponsePayload, Pagination
from app.utils.security import create_access_token, create_refresh_token, get_password_hash
from app.config import settings
from app.utils.role_utils import convert_role_to_string
from datetime import datetime
import humanize
import random

router = APIRouter()

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_users(db: AsyncSession, offset: int = 0, limit: int = 10) -> List[User]:
    result = await db.execute(select(User).offset(offset).limit(limit))
    # result = await db.execute(select(User).offset(offset).limit(limit).options(selectinload(User.profile)))
    return result.scalars().all()

def generate_initial(full_name: str):
    label = full_name[0].upper() if full_name else "U"
    state = random.choice(["danger", "warning", "primary"])
    return {"label": label, "state": state}

async def get_users_with_profiles(db: AsyncSession, offset: int = 0, limit: int = 10) -> List[UserProfileRead]:
    result = await db.execute(
        select(User)
        .offset(offset)
        .limit(limit)
        .options(selectinload(User.profile))
    )
    users = result.scalars().all()
    user_profiles = []

    for user in users:
        if user.profile and user.profile.avatar:
            avatar = user.profile.avatar
        else:
            avatar = generate_initial(user.full_name)
        
        profile = None
        if user.profile:
            profile = ProfileRead(
                id=user.profile.id,
                user_id=user.profile.user_id,
                company=user.profile.company,
                phone=user.profile.phone,
                country=user.profile.country,
            )
            
        user_profile = UserProfileRead(
                id=user.id,
                name=user.full_name,
                email=user.email,
                role=convert_role_to_string(user.role),
                joined_day=humanize.naturaltime(user.created_at),
                updated_at=user.updated_at,
                last_login=humanize.naturaltime(datetime.utcnow() - user.last_logged_in) if user.last_logged_in else None,
                profile=profile
            )
        if user.profile.avatar == "":
            user_profile.initials = avatar
        else:
            user_profile.avatar = avatar
        
        user_profiles.append(
            user_profile
        )
    return user_profiles

@router.post("/", response_model=Token)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user_by_username = await get_user_by_username(db, user.username)
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )
    
    existing_user_by_email = await get_user_by_email(db, user.email)
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username, email=user.email, full_name=user.full_name, role=user.role, hashed_password=hashed_password
    )
    db.add(db_user)
    await db.flush()
    db_profile = Profile(
        user_id=db_user.id,
        company="",
        phone="",
        country="",
        avatar=""
    )
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_user)
    user = await authenticate_user(db, user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "bearer"},
        )
    await update_last_logged_in(db, user.id)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"email": user.email}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"email": user.email}, expires_delta=refresh_token_expires)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/{user_id}", response_model=UserProfileRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(User).filter(User.id == user_id).options(selectinload(User.profile)))
    user = results.scalars().first()
    if user.profile and user.profile.avatar:
        avatar = user.profile.avatar
    else:
        avatar = generate_initial(user.full_name)
    user_profile = UserProfileRead(
        id=user.id,
        name=user.full_name,
        email=user.email,
        role=convert_role_to_string(user.role)
    )
    if user.profile.avatar == "":
        user_profile.initials = avatar
    else:
        user_profile.avatar = avatar
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_profile

@router.get("/", response_model=UserResponse)
async def read_users(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    items_per_page: int = Query(10, ge=1, le=100, description="Number of items per page")
):
    offset = (page - 1) * items_per_page
    users = await get_users_with_profiles(db, offset=offset, limit=items_per_page)
    
    total_users = await db.execute(select(func.count(User.id)))
    total = total_users.scalar()

    last_page = (total + items_per_page - 1) // items_per_page
    from_item = offset + 1
    to_item = min(offset + items_per_page, total)

    response = UserResponse(
        data=users,
        payload=ResponsePayload(
            pagination=Pagination(
                from_item=from_item,
                last_page=last_page,
                page=page,
                total=total,
                to=to_item
            )
        )
    )
    
    return response

@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    db_user = await db.execute(select(User).filter(User.id == user_id)).scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for var, value in vars(user).items():
        setattr(db_user, var, value) if value else None
    if user.password:
        db_user.hashed_password = get_password_hash(user.password)
    db_user.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", response_model=UserRead)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).filter(User.id == user_id)).scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return user
