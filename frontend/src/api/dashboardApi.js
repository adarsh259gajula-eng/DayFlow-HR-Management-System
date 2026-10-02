import axiosClient, { getApiBaseUrl } from './axiosClient';

export const dashboardApi = {
  getEmployeeDashboard: () => axiosClient.get('/dashboard/employee'),
  getAdminDashboard: () => axiosClient.get('/dashboard/admin'),
};

export const reportsApi = {
  getPaystubPdfUrl: (slipId) => `${getApiBaseUrl()}/reports/paystub/${slipId}/pdf`,
  getAttendanceCsvUrl: (month) => `${getApiBaseUrl()}/reports/attendance/csv?month=${month}`,
  getPayrollCsvUrl: (month) => `${getApiBaseUrl()}/reports/payroll/csv?month=${month}`,
  getLeaveCsvUrl: (month) => `${getApiBaseUrl()}/reports/leave/csv${month ? `?month=${month}` : ''}`,
  getEmployeesCsvUrl: () => `${getApiBaseUrl()}/reports/employees/csv`,
};
