import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import apiClient from '@/lib/api';

export default function Dashboard() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const data = await apiClient.healthCheck();
      setHealth(data);
    } catch (err) {
      console.error('Health check failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <h1 className="text-3xl font-bold text-gray-900">FinGuard AI</h1>
          <p className="text-gray-600">Enterprise Fintech Platform</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-12">
        {/* Status Card */}
        <div className="mb-8 p-6 bg-white rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">System Status</h2>
          {loading ? (
            <p className="text-gray-500">Checking...</p>
          ) : health ? (
            <div className="space-y-2">
              <p className="flex items-center">
                <span className="w-3 h-3 bg-green-500 rounded-full mr-2"></span>
                <span>
                  API: <strong>{health.status}</strong>
                </span>
              </p>
              <p className="flex items-center">
                <span className={`w-3 h-3 rounded-full mr-2 ${health.db === 'connected' ? 'bg-green-500' : 'bg-red-500'}`}></span>
                <span>Database: <strong>{health.db}</strong></span>
              </p>
              <p className="flex items-center">
                <span className={`w-3 h-3 rounded-full mr-2 ${health.redis === 'connected' ? 'bg-green-500' : 'bg-red-500'}`}></span>
                <span>Redis: <strong>{health.redis}</strong></span>
              </p>
            </div>
          ) : (
            <p className="text-red-600">Unable to connect to API</p>
          )}
        </div>

        {/* Navigation Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link href="/vendors">
            <div className="p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition cursor-pointer">
              <h3 className="text-xl font-semibold text-blue-600 mb-2">Vendors</h3>
              <p className="text-gray-600">Manage vendors and risk scores</p>
            </div>
          </Link>

          <Link href="/invoices">
            <div className="p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition cursor-pointer">
              <h3 className="text-xl font-semibold text-green-600 mb-2">Invoices</h3>
              <p className="text-gray-600">Track invoices and anomalies</p>
            </div>
          </Link>

          <Link href="/audit">
            <div className="p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition cursor-pointer">
              <h3 className="text-xl font-semibold text-purple-600 mb-2">Audit Logs</h3>
              <p className="text-gray-600">View ML predictions and actions</p>
            </div>
          </Link>
        </div>

        {/* Quick Stats */}
        <div className="mt-12 p-6 bg-white rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Features</h2>
          <ul className="space-y-2 text-gray-700">
            <li className="flex items-center">
              <span className="w-2 h-2 bg-blue-600 rounded-full mr-3"></span>
              Real-time anomaly detection using Isolation Forest
            </li>
            <li className="flex items-center">
              <span className="w-2 h-2 bg-blue-600 rounded-full mr-3"></span>
              Late payment risk prediction with XGBoost
            </li>
            <li className="flex items-center">
              <span className="w-2 h-2 bg-blue-600 rounded-full mr-3"></span>
              Comprehensive audit logging for compliance
            </li>
            <li className="flex items-center">
              <span className="w-2 h-2 bg-blue-600 rounded-full mr-3"></span>
              Async PostgreSQL with connection pooling
            </li>
            <li className="flex items-center">
              <span className="w-2 h-2 bg-blue-600 rounded-full mr-3"></span>
              Redis caching for optimal performance
            </li>
          </ul>
        </div>
      </main>
    </div>
  );
}
