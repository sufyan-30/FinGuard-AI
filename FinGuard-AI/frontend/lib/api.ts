"""API service client library"""

import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  // Vendors
  async getVendors(page: number = 1, pageSize: number = 10) {
    const response = await this.client.get('/vendors', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  }

  async getVendor(id: number) {
    const response = await this.client.get(`/vendors/${id}`);
    return response.data;
  }

  async createVendor(data: any) {
    const response = await this.client.post('/vendors', data);
    return response.data;
  }

  async updateVendor(id: number, data: any) {
    const response = await this.client.put(`/vendors/${id}`, data);
    return response.data;
  }

  async deleteVendor(id: number) {
    await this.client.delete(`/vendors/${id}`);
  }

  // Invoices
  async getInvoices(page: number = 1, pageSize: number = 10, filters?: any) {
    const response = await this.client.get('/invoices', {
      params: { page, page_size: pageSize, ...filters },
    });
    return response.data;
  }

  async getInvoice(id: number) {
    const response = await this.client.get(`/invoices/${id}`);
    return response.data;
  }

  async createInvoice(data: any) {
    const response = await this.client.post('/invoices', data);
    return response.data;
  }

  async updateInvoice(id: number, data: any) {
    const response = await this.client.put(`/invoices/${id}`, data);
    return response.data;
  }

  async detectAnomaly(invoiceId: number) {
    const response = await this.client.post(`/invoices/${invoiceId}/detect-anomaly`);
    return response.data;
  }

  // Audit Logs
  async getAuditLogs(page: number = 1, pageSize: number = 10, filters?: any) {
    const response = await this.client.get('/audit-logs', {
      params: { page, page_size: pageSize, ...filters },
    });
    return response.data;
  }

  async getVendorAuditLogs(vendorId: number, page: number = 1, pageSize: number = 10) {
    const response = await this.client.get(`/audit-logs/vendor/${vendorId}`, {
      params: { page, page_size: pageSize },
    });
    return response.data;
  }

  // Health Check
  async healthCheck() {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      return { status: 'unhealthy', error: String(error) };
    }
  }
}

export default new APIClient();
