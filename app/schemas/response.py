from pydantic import BaseModel
from typing import List
from app.schemas.profile import UserProfileRead

class Pagination(BaseModel):
    from_item: int
    last_page: int
    page: int
    total: int
    to: int

class ResponsePayload(BaseModel):
    pagination: Pagination

class UserResponse(BaseModel):
    data: List[UserProfileRead]
    payload: ResponsePayload
