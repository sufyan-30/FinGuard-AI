"""Invoice API routes with anomaly detection"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from backend.database import get_db, Invoice, Vendor, AuditLog
from backend.models import InvoiceCreate, InvoiceUpdate, InvoiceResponse, AnomalyDetectionResult, PaginatedResponse
from ml_models import anomaly_detector, risk_predictor
from datetime import datetime
import pytz
import numpy as np

router = APIRouter(prefix="/api/invoices", tags=["invoices"])


@router.post("", response_model=InvoiceResponse, status_code=201)
async def create_invoice(invoice: InvoiceCreate, db: AsyncSession = Depends(get_db)):
    """Create invoice with anomaly detection"""
    vendor_result = await db.execute(select(Vendor).where(Vendor.id == invoice.vendor_id))
    vendor = vendor_result.scalar_one_or_none()

    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    # Prepare features for ML models
    features = np.array([[
        float(invoice.amount),
        (invoice.due_date - invoice.issue_date).days,
        vendor.risk_score,
    ]])

    # Detect anomaly
    is_anomaly = False
    anomaly_confidence = 0.0
    if anomaly_detector.is_trained:
        try:
            is_anomaly, anomaly_confidence = anomaly_detector.predict_single(features[0].tolist())
        except:
            pass

    # Predict risk
    late_risk = 0.0
    if risk_predictor.is_trained:
        try:
            late_risk = risk_predictor.predict_single(features[0].tolist())
        except:
            pass

    db_invoice = Invoice(
        vendor_id=invoice.vendor_id,
        amount=invoice.amount,
        issue_date=invoice.issue_date,
        due_date=invoice.due_date,
        status="pending",
        is_anomaly=is_anomaly,
        late_risk_probability=late_risk,
        description=invoice.description,
        created_at=datetime.now(pytz.UTC),
    )

    db.add(db_invoice)
    await db.commit()
    await db.refresh(db_invoice)

    # Log prediction
    audit_log = AuditLog(
        vendor_id=invoice.vendor_id,
        invoice_id=db_invoice.id,
        action="invoice_created_with_prediction",
        model_type="anomaly_detection,risk_prediction",
        prediction=float(anomaly_confidence),
        confidence=late_risk,
        details=f"Anomaly: {is_anomaly}, Risk: {late_risk}",
        created_at=datetime.now(pytz.UTC),
    )
    db.add(audit_log)
    await db.commit()

    return db_invoice


@router.get("", response_model=PaginatedResponse)
async def list_invoices(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    vendor_id: int = Query(None),
    status: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """List invoices with filtering"""
    query = select(Invoice)

    if vendor_id:
        query = query.where(Invoice.vendor_id == vendor_id)
    if status:
        query = query.where(Invoice.status == status)

    total_result = await db.execute(query)
    total = len(total_result.scalars().all())

    offset = (page - 1) * page_size
    result = await db.execute(
        query.offset(offset).limit(page_size).order_by(desc(Invoice.created_at))
    )
    invoices = result.scalars().all()

    return PaginatedResponse(
        items=[InvoiceResponse.model_validate(i) for i in invoices],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(invoice_id: int, db: AsyncSession = Depends(get_db)):
    """Get invoice by ID"""
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice = result.scalar_one_or_none()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.put("/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_id: int, invoice: InvoiceUpdate, db: AsyncSession = Depends(get_db)
):
    """Update invoice status"""
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    db_invoice = result.scalar_one_or_none()

    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    update_data = invoice.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_invoice, field, value)

    db_invoice.updated_at = datetime.now(pytz.UTC)
    await db.commit()
    await db.refresh(db_invoice)
    return db_invoice


@router.post("/{invoice_id}/detect-anomaly", response_model=AnomalyDetectionResult)
async def detect_anomaly_endpoint(invoice_id: int, db: AsyncSession = Depends(get_db)):
    """Re-run anomaly detection on invoice"""
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice = result.scalar_one_or_none()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if not anomaly_detector.is_trained:
        raise HTTPException(status_code=400, detail="Anomaly detector not trained")

    vendor_result = await db.execute(select(Vendor).where(Vendor.id == invoice.vendor_id))
    vendor = vendor_result.scalar_one_or_none()

    features = np.array([[
        float(invoice.amount),
        (invoice.due_date - invoice.issue_date).days,
        vendor.risk_score if vendor else 0.0,
    ]])

    is_anomaly, confidence = anomaly_detector.predict_single(features[0].tolist())
    risk_score = confidence * 100

    invoice.is_anomaly = is_anomaly
    await db.commit()

    return AnomalyDetectionResult(
        invoice_id=invoice_id,
        is_anomaly=is_anomaly,
        confidence=confidence,
        risk_score=risk_score,
    )
