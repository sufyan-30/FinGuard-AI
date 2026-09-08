"""Vendor API routes"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from backend.database import get_db, Vendor
from backend.models import VendorCreate, VendorUpdate, VendorResponse, PaginatedResponse
from datetime import datetime
import pytz

router = APIRouter(prefix="/api/vendors", tags=["vendors"])


@router.post("", response_model=VendorResponse, status_code=201)
async def create_vendor(vendor: VendorCreate, db: AsyncSession = Depends(get_db)):
    """Create new vendor"""
    db_vendor = Vendor(
        name=vendor.name,
        email=vendor.email,
        phone=vendor.phone,
        country=vendor.country,
        created_at=datetime.now(pytz.UTC),
    )
    db.add(db_vendor)
    await db.commit()
    await db.refresh(db_vendor)
    return db_vendor


@router.get("", response_model=PaginatedResponse)
async def list_vendors(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List vendors with pagination"""
    offset = (page - 1) * page_size

    total_result = await db.execute(select(Vendor))
    total = len(total_result.scalars().all())

    result = await db.execute(
        select(Vendor).offset(offset).limit(page_size).order_by(desc(Vendor.created_at))
    )
    vendors = result.scalars().all()

    return PaginatedResponse(
        items=[VendorResponse.model_validate(v) for v in vendors],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{vendor_id}", response_model=VendorResponse)
async def get_vendor(vendor_id: int, db: AsyncSession = Depends(get_db)):
    """Get vendor by ID"""
    result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
    vendor = result.scalar_one_or_none()

    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@router.put("/{vendor_id}", response_model=VendorResponse)
async def update_vendor(
    vendor_id: int, vendor: VendorUpdate, db: AsyncSession = Depends(get_db)
):
    """Update vendor"""
    result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
    db_vendor = result.scalar_one_or_none()

    if not db_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    update_data = vendor.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_vendor, field, value)

    db_vendor.updated_at = datetime.now(pytz.UTC)
    await db.commit()
    await db.refresh(db_vendor)
    return db_vendor


@router.delete("/{vendor_id}", status_code=204)
async def delete_vendor(vendor_id: int, db: AsyncSession = Depends(get_db)):
    """Delete vendor"""
    result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
    db_vendor = result.scalar_one_or_none()

    if not db_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    await db.delete(db_vendor)
    await db.commit()
