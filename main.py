import asyncio
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from sqlalchemy import select
from app.routers import auth, users, products, profile, marketplace, utils, orders
from app.database import Base, engine
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.refresh_products import refresh_products
from app.models.marketplace import Marketplace

# member
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
# from module import Member, get_member, check_access

app = FastAPI()

class MemberResponse(BaseModel):
    username: str
    role_name: str
    access_level: str

# @app.get("/members/{username}", response_model=MemberResponse)
# def get_member_details(username: str):
#     member = get_member(username)
#     if member is None:
#         raise HTTPException(status_code=404, detail="Member not found")
#     return {
#         "username": member.username,
#         "role_name": member.role.name,
#         "access_level": member.role.access_level
#     }

# @app.get("/members/{username}/access-check")
# def check_member_access(username: str, feature: str):
#     member = get_member(username)
#     if member is None:
#         raise HTTPException(status_code=404, detail="Member not found")
    
#     if check_access(member, feature):
#         return {"access_granted": True}
#     else:
#         return {"access_granted": False}

# member


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await init_models()

@app.on_event("startup")
@repeat_every(seconds=900)  # Run daily for deleting video last 30 days
async def refresh_products(db: AsyncSession = Depends(get_db)):
    marketplaces = await db.execute(select(Marketplace)).scalars().all()
    for marketplace in marketplaces:
        refresh_products(marketplace)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(marketplace.router, prefix="/api/marketplace", tags=["marketplace"])
app.include_router(utils.router, prefix="/api/utils", tags=["utils"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
