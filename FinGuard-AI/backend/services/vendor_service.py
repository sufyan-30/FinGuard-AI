"""Vendor service layer"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database import Vendor, Invoice
from backend.models import VendorCreate, VendorUpdate
from datetime import datetime
import pytz


class VendorService:
    """Business logic for vendor operations"""

    @staticmethod
    async def calculate_risk_score(db: AsyncSession, vendor_id: int) -> float:
        """Calculate vendor risk score from invoices"""
        result = await db.execute(
            select(Invoice).where(Invoice.vendor_id == vendor_id)
        )
        invoices = result.scalars().all()

        if not invoices:
            return 0.0

        anomaly_count = sum(1 for inv in invoices if inv.is_anomaly)
        avg_risk = sum(inv.late_risk_probability for inv in invoices) / len(invoices)
        anomaly_rate = anomaly_count / len(invoices)

        risk_score = (avg_risk * 0.6 + anomaly_rate * 0.4) * 100
        return min(100.0, risk_score)

    @staticmethod
    async def update_vendor_risk(db: AsyncSession, vendor_id: int) -> None:
        """Update vendor risk score"""
        result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
        vendor = result.scalar_one_or_none()

        if vendor:
            risk_score = await VendorService.calculate_risk_score(db, vendor_id)
            vendor.risk_score = risk_score
            vendor.updated_at = datetime.now(pytz.UTC)
            await db.commit()


vendor_service = VendorService()
