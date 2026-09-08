import React, { useState, useEffect } from 'react';
import apiClient from '@/lib/api';

export default function AuditLogs() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [vendorFilter, setVendorFilter] = useState(null);

  useEffect(() => {
    fetchLogs();
  }, [vendorFilter]);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const filters = vendorFilter ? { vendor_id: vendorFilter } : {};
      const data = await apiClient.getAuditLogs(1, 20, filters);
      setLogs(data.items || []);
      setError(null);
    } catch (err) {
      setError('Failed to load audit logs');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Audit Logs</h1>

      {error && <p className="text-red-600 mb-4">{error}</p>}

      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="border-b-2 bg-gray-50">
                <th className="p-3 text-left">Timestamp</th>
                <th className="p-3 text-left">Vendor ID</th>
                <th className="p-3 text-left">Invoice ID</th>
                <th className="p-3 text-left">Action</th>
                <th className="p-3 text-left">Model</th>
                <th className="p-3 text-left">Prediction</th>
                <th className="p-3 text-left">Confidence</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={log.id} className="border-b hover:bg-gray-50">
                  <td className="p-3 text-xs">{formatDate(log.created_at)}</td>
                  <td className="p-3">{log.vendor_id}</td>
                  <td className="p-3">{log.invoice_id || '-'}</td>
                  <td className="p-3 font-medium">{log.action}</td>
                  <td className="p-3 text-xs">{log.model_type || '-'}</td>
                  <td className="p-3">
                    {log.prediction !== null ? (log.prediction * 100).toFixed(1) + '%' : '-'}
                  </td>
                  <td className="p-3">
                    {log.confidence !== null ? (log.confidence * 100).toFixed(1) + '%' : '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
