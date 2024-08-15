from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

class Attachment(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    visibility: Optional[str] = None
    type: Optional[str] = None
    force_download: Optional[str] = None

class Flag(BaseModel):
    flag: Optional[str] = None
    value: Optional[str] = None

class Detail(BaseModel):
    locker_delivery_eligible: Optional[str] = None
    locker_id: Optional[str] = None
    locker_name: Optional[str] = None

class OrderBase(BaseModel):
    vendor_name: Optional[str] = None
    type: Optional[int] = None
    parent_id: Optional[int] = None
    date: Optional[datetime] = None
    payment_mode: Optional[str] = None
    detailed_payment_method: Optional[str] = None
    delivery_mode: Optional[str] = None
    observation: Optional[str] = None
    status: Optional[int] = None
    payment_status: Optional[int] = None
    customer_id: Optional[int] = None
    product_id: Optional[str] = None
    shipping_tax: Optional[float] = None
    shipping_tax_voucher_split: Optional[str] = None
    vouchers: Optional[str] = None
    proforms: Optional[str] = None
    attachments: Optional[str] = None
    cashed_co: Optional[float] = None
    cashed_cod: Optional[float] = None
    cancellation_request: Optional[str] = None
    has_editable_products: Optional[float] = None
    refunded_amount: Optional[float] = None
    is_complete: Optional[int] = None
    reason_cancellation: Optional[str] = None
    refund_status: Optional[str] = None
    maximum_date_for_shipment: Optional[datetime] = None
    late_shipment: Optional[int] = None
    flags: Optional[str] = None
    emag_club: Optional[int] = None
    finalization_date: Optional[datetime] = None
    details: Optional[str] = None
    weekend_delivery: Optional[int] = None
    payment_mode_id: Optional[int] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int

    class Config:
        orm_mode = True
