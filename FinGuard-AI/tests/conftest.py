"""Pytest configuration and fixtures"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.database import Base
import os

# Test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def test_db():
    """Create test database and tables"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncTestingSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncTestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def sample_vendor(test_db):
    """Create sample vendor"""
    from backend.database import Vendor
    from datetime import datetime
    import pytz

    vendor = Vendor(
        name="Test Vendor Inc.",
        email="vendor@test.com",
        phone="+1234567890",
        country="USA",
        risk_score=25.0,
        created_at=datetime.now(pytz.UTC),
    )
    test_db.add(vendor)
    await test_db.commit()
    await test_db.refresh(vendor)
    return vendor


@pytest.fixture
async def sample_invoice(test_db, sample_vendor):
    """Create sample invoice"""
    from backend.database import Invoice
    from datetime import datetime, timedelta
    import pytz

    invoice = Invoice(
        vendor_id=sample_vendor.id,
        amount=1000.00,
        issue_date=datetime.now(pytz.UTC),
        due_date=datetime.now(pytz.UTC) + timedelta(days=30),
        status="pending",
        is_anomaly=False,
        late_risk_probability=0.15,
        created_at=datetime.now(pytz.UTC),
    )
    test_db.add(invoice)
    await test_db.commit()
    await test_db.refresh(invoice)
    return invoice


pytest_plugins = ("pytest_asyncio",)
