"""Audit Log API routes"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from backend.database import get_db, AuditLog
from backend.models import AuditLogResponse, PaginatedResponse

router = APIRouter(prefix="/api/audit-logs", tags=["audit"])


@router.get("", response_model=PaginatedResponse)
async def list_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    vendor_id: int = Query(None),
    model_type: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """List audit logs with filtering"""
    query = select(AuditLog)

    if vendor_id:
        query = query.where(AuditLog.vendor_id == vendor_id)
    if model_type:
        query = query.where(AuditLog.model_type == model_type)

    total_result = await db.execute(query)
    total = len(total_result.scalars().all())

    offset = (page - 1) * page_size
    result = await db.execute(
        query.offset(offset).limit(page_size).order_by(desc(AuditLog.created_at))
    )
    logs = result.scalars().all()

    return PaginatedResponse(
        items=[AuditLogResponse.model_validate(l) for l in logs],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/vendor/{vendor_id}", response_model=PaginatedResponse)
async def list_vendor_audit_logs(
    vendor_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List audit logs for specific vendor"""
    query = select(AuditLog).where(AuditLog.vendor_id == vendor_id)

    total_result = await db.execute(query)
    total = len(total_result.scalars().all())

    offset = (page - 1) * page_size
    result = await db.execute(
        query.offset(offset).limit(page_size).order_by(desc(AuditLog.created_at))
    )
    logs = result.scalars().all()

    return PaginatedResponse(
        items=[AuditLogResponse.model_validate(l) for l in logs],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )
