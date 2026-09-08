"""Invoice service layer"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database import Invoice, AuditLog
from backend.services.vendor_service import vendor_service
from datetime import datetime
import pytz


class InvoiceService:
    """Business logic for invoice operations"""

    @staticmethod
    async def record_prediction(
        db: AsyncSession,
        invoice_id: int,
        vendor_id: int,
        model_type: str,
        prediction: float,
        confidence: float,
        details: str,
    ) -> None:
        """Log ML prediction to audit trail"""
        audit_log = AuditLog(
            vendor_id=vendor_id,
            invoice_id=invoice_id,
            action="ml_prediction",
            model_type=model_type,
            prediction=prediction,
            confidence=confidence,
            details=details,
            created_at=datetime.now(pytz.UTC),
        )
        db.add(audit_log)
        await db.commit()

    @staticmethod
    async def update_invoice_status(
        db: AsyncSession, invoice_id: int, status: str
    ) -> None:
        """Update invoice status and recalculate vendor risk"""
        result = await db.execute(
            select(Invoice).where(Invoice.id == invoice_id)
        )
        invoice = result.scalar_one_or_none()

        if invoice:
            invoice.status = status
            invoice.updated_at = datetime.now(pytz.UTC)
            await db.commit()

            # Recalculate vendor risk
            await vendor_service.update_vendor_risk(db, invoice.vendor_id)


invoice_service = InvoiceService()
