"""SQLAlchemy ORM Models"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Numeric, ForeignKey, Index, UniqueConstraint, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import pytz

Base = declarative_base()


class Vendor(Base):
    """Vendor/Supplier model with risk scoring"""
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)
    risk_score = Column(Float, default=0.0, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.UTC), index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(pytz.UTC), onupdate=lambda: datetime.now(pytz.UTC))

    invoices = relationship("Invoice", back_populates="vendor", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="vendor", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_vendor_name_risk", "name", "risk_score"),
        Index("idx_vendor_created", "created_at"),
    )


class Invoice(Base):
    """Invoice model with anomaly detection flags"""
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False, index=True)
    amount = Column(Numeric(15, 2), nullable=False)
    issue_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False, index=True)
    status = Column(String(50), default="pending", index=True)
    is_anomaly = Column(Boolean, default=False, index=True)
    late_risk_probability = Column(Float, default=0.0, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.UTC), index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(pytz.UTC), onupdate=lambda: datetime.now(pytz.UTC))

    vendor = relationship("Vendor", back_populates="invoices")
    audit_logs = relationship("AuditLog", back_populates="invoice", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_invoice_vendor_status", "vendor_id", "status"),
        Index("idx_invoice_anomaly", "is_anomaly"),
        Index("idx_invoice_risk", "late_risk_probability"),
        UniqueConstraint("vendor_id", "issue_date", "amount", name="uq_invoice_vendor_date_amount"),
    )


class AuditLog(Base):
    """Audit log for ML predictions and system actions"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True, index=True)
    action = Column(String(100), nullable=False)
    model_type = Column(String(50), nullable=True)
    prediction = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.UTC), index=True)

    vendor = relationship("Vendor", back_populates="audit_logs")
    invoice = relationship("Invoice", back_populates="audit_logs")

    __table_args__ = (
        Index("idx_audit_vendor_action", "vendor_id", "action"),
        Index("idx_audit_model", "model_type"),
        Index("idx_audit_created", "created_at"),
    )
