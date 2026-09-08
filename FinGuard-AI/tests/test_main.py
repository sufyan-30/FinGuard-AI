"""Test suite for main API"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_create_vendor(test_db):
    """Test vendor creation"""
    vendor_data = {
        "name": "New Vendor LLC",
        "email": "new@vendor.com",
        "phone": "+9876543210",
        "country": "Canada",
    }
    response = client.post("/api/vendors", json=vendor_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == vendor_data["name"]
    assert data["email"] == vendor_data["email"]


@pytest.mark.asyncio
async def test_list_vendors(test_db, sample_vendor):
    """Test vendor listing"""
    response = client.get("/api/vendors?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_get_vendor(test_db, sample_vendor):
    """Test get vendor by ID"""
    response = client.get(f"/api/vendors/{sample_vendor.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_vendor.id


@pytest.mark.asyncio
async def test_create_invoice(test_db, sample_vendor):
    """Test invoice creation"""
    from datetime import datetime, timedelta
    import pytz

    invoice_data = {
        "vendor_id": sample_vendor.id,
        "amount": "5000.00",
        "issue_date": datetime.now(pytz.UTC).isoformat(),
        "due_date": (datetime.now(pytz.UTC) + timedelta(days=30)).isoformat(),
    }
    response = client.post("/api/invoices", json=invoice_data)
    assert response.status_code == 201
    data = response.json()
    assert data["vendor_id"] == sample_vendor.id


@pytest.mark.asyncio
async def test_list_invoices(test_db, sample_invoice):
    """Test invoice listing"""
    response = client.get("/api/invoices?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


@pytest.mark.asyncio
async def test_list_audit_logs(test_db):
    """Test audit log listing"""
    response = client.get("/api/audit-logs?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
