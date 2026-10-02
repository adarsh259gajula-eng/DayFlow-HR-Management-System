import axiosClient from './axiosClient';

export const dashboardApi = {
  getEmployeeDashboard: () => axiosClient.get('/dashboard/employee'),
  getAdminDashboard: () => axiosClient.get('/dashboard/admin'),
};

const apiPrefix = (import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/$/, '');
const normalizedPrefix = apiPrefix.endsWith('/api') ? apiPrefix : `${apiPrefix}/api`;

export const reportsApi = {
  getPaystubPdfUrl: (slipId) => `${normalizedPrefix}/reports/paystub/${slipId}/pdf`,
  getAttendanceCsvUrl: (month) => `${normalizedPrefix}/reports/attendance/csv?month=${month}`,
  getPayrollCsvUrl: (month) => `${normalizedPrefix}/reports/payroll/csv?month=${month}`,
  getLeaveCsvUrl: (month) => `${normalizedPrefix}/reports/leave/csv${month ? `?month=${month}` : ''}`,
  getEmployeesCsvUrl: () => `${normalizedPrefix}/reports/employees/csv`,
};
