import React, { useState, useEffect } from 'react';
import apiClient from '@/lib/api';

export default function VendorDashboard() {
  const [vendors, setVendors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchVendors();
  }, []);

  const fetchVendors = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getVendors(1, 10);
      setVendors(data.items || []);
      setError(null);
    } catch (err) {
      setError('Failed to load vendors');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateVendor = async () => {
    const vendorName = prompt('Enter vendor name:');
    if (!vendorName) return;

    try {
      await apiClient.createVendor({ name: vendorName });
      await fetchVendors();
    } catch (err) {
      alert('Failed to create vendor');
    }
  };

  const handleDeleteVendor = async (id) => {
    if (!confirm('Are you sure?')) return;

    try {
      await apiClient.deleteVendor(id);
      await fetchVendors();
    } catch (err) {
      alert('Failed to delete vendor');
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Vendors</h1>
        <button
          onClick={handleCreateVendor}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-semibold transition"
        >
          + Add Vendor
        </button>
      </div>

      {error && <p className="text-red-600 mb-4">{error}</p>}

      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <div className="grid gap-4">
          {vendors.map((vendor) => (
            <div key={vendor.id} className="border p-4 rounded-lg bg-white shadow-sm">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-semibold">{vendor.name}</h3>
                  <p className="text-gray-600">Risk Score: {vendor.risk_score.toFixed(2)}</p>
                </div>
                <button
                  onClick={() => handleDeleteVendor(vendor.id)}
                  className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm transition"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
