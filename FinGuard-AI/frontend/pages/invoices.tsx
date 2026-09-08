import React, { useState, useEffect } from 'react';
import apiClient from '@/lib/api';

export default function InvoicesDashboard() {
  const [invoices, setInvoices] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<string | null>(null);

  useEffect(() => {
    fetchInvoices();
  }, [statusFilter]);

  const fetchInvoices = async () => {
    try {
      setLoading(true);
      const filters = statusFilter ? { status: statusFilter } : {};
      const data = await apiClient.getInvoices(1, 10, filters);
      setInvoices(data.items || []);
      setError(null);
    } catch (err) {
      setError('Failed to load invoices');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (id: number, newStatus: string) => {
    try {
      await apiClient.updateInvoice(id, { status: newStatus });
      await fetchInvoices();
    } catch (err) {
      alert('Failed to update invoice');
    }
  };

  const handleDetectAnomaly = async (id: number) => {
    try {
      const result = await apiClient.detectAnomaly(id);
      alert(`Anomaly: ${result.is_anomaly}, Confidence: ${(result.confidence * 100).toFixed(2)}%`);
      await fetchInvoices();
    } catch (err) {
      alert('Failed to detect anomaly');
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Invoices</h1>

      <div className="mb-4 flex gap-2">
        <button
          onClick={() => setStatusFilter(null)}
          className={`px-3 py-1 rounded text-sm font-semibold transition ${
            statusFilter === null ? 'bg-blue-600 text-white' : 'bg-gray-200'
          }`}
        >
          All
        </button>
        {['pending', 'paid', 'overdue', 'disputed'].map((status) => (
          <button
            key={status}
            onClick={() => setStatusFilter(status)}
            className={`px-3 py-1 rounded text-sm font-semibold transition ${
              statusFilter === status ? 'bg-blue-600 text-white' : 'bg-gray-200'
            }`}
          >
            {status.charAt(0).toUpperCase() + status.slice(1)}
          </button>
        ))}
      </div>

      {error && <p className="text-red-600 mb-4">{error}</p>}

      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="border-b-2 bg-gray-50">
                <th className="p-3 text-left">ID</th>
                <th className="p-3 text-left">Amount</th>
                <th className="p-3 text-left">Status</th>
                <th className="p-3 text-left">Anomaly</th>
                <th className="p-3 text-left">Risk</th>
                <th className="p-3 text-left">Due Date</th>
                <th className="p-3 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {invoices.map((invoice) => (
                <tr key={invoice.id} className="border-b hover:bg-gray-50">
                  <td className="p-3">{invoice.id}</td>
                  <td className="p-3">${parseFloat(invoice.amount).toFixed(2)}</td>
                  <td className="p-3">
                    <select
                      value={invoice.status}
                      onChange={(e) => handleStatusUpdate(invoice.id, e.target.value)}
                      className="border px-2 py-1 rounded"
                    >
                      <option value="pending">Pending</option>
                      <option value="paid">Paid</option>
                      <option value="overdue">Overdue</option>
                      <option value="disputed">Disputed</option>
                    </select>
                  </td>
                  <td className="p-3">
                    <span
                      className={`px-2 py-1 rounded text-xs font-semibold ${
                        invoice.is_anomaly ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                      }`}
                    >
                      {invoice.is_anomaly ? 'Yes' : 'No'}
                    </span>
                  </td>
                  <td className="p-3">{(invoice.late_risk_probability * 100).toFixed(1)}%</td>
                  <td className="p-3">{formatDate(invoice.due_date)}</td>
                  <td className="p-3">
                    <button
                      onClick={() => handleDetectAnomaly(invoice.id)}
                      className="bg-purple-600 hover:bg-purple-700 text-white px-2 py-1 rounded text-xs transition"
                    >
                      Scan
                    </button>
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
