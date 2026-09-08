"""Pydantic v2 request/response schemas"""

from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

# Vendor Schemas
class VendorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)


class VendorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    risk_score: Optional[float] = Field(None, ge=0, le=100)


class VendorResponse(BaseModel):
    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    country: Optional[str]
    risk_score: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Invoice Schemas
class InvoiceCreate(BaseModel):
    vendor_id: int
    amount: Decimal = Field(..., decimal_places=2, gt=0)
    issue_date: datetime
    due_date: datetime
    description: Optional[str] = None

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v, info):
        if "issue_date" in info.data and v <= info.data["issue_date"]:
            raise ValueError("due_date must be after issue_date")
        return v


class InvoiceUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(pending|paid|overdue|disputed)$")
    amount: Optional[Decimal] = Field(None, decimal_places=2, gt=0)
    description: Optional[str] = None


class InvoiceResponse(BaseModel):
    id: int
    vendor_id: int
    amount: Decimal
    issue_date: datetime
    due_date: datetime
    status: str
    is_anomaly: bool
    late_risk_probability: float
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# AuditLog Schemas
class AuditLogResponse(BaseModel):
    id: int
    vendor_id: int
    invoice_id: Optional[int]
    action: str
    model_type: Optional[str]
    prediction: Optional[float]
    confidence: Optional[float]
    details: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
        protected_namespaces = ()   # ye line add karo

# Anomaly Detection Response
class AnomalyDetectionResult(BaseModel):
    invoice_id: int
    is_anomaly: bool
    confidence: float = Field(..., ge=0, le=1)
    risk_score: float = Field(..., ge=0, le=100)
    details: Optional[str] = None


# Pagination
class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int


# Health Check Response
class HealthCheckResponse(BaseModel):
    status: str
    db: str
    redis: str
    timestamp: datetime
