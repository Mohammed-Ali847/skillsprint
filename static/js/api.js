// static/js/api.js - API & State Management
const API_BASE = '/api';

const state = {
  currentRole: 'admin',
  currentTab: 'dashboard',
  selectedEmployeeId: 1,
  selectedPlanId: 1,
  selectedQuizId: null,
  activeQuizData: null,
  employees: [],
  roles: [],
  documents: [],
  activePlan: null,
  complianceReport: null
};

async function fetchAPI(endpoint, options = {}) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {})
      },
      ...options
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'API request failed');
    }
    return await res.json();
  } catch (error) {
    showToast(error.message, 'error');
    console.error('Fetch error:', error);
    throw error;
  }
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  const bg = type === 'error' ? 'bg-rose-950/90 border-rose-500 text-rose-200' : (type === 'success' ? 'bg-emerald-950/90 border-emerald-500 text-emerald-200' : 'bg-blue-950/90 border-blue-500 text-blue-200');
  toast.className = `flex items-center gap-3 px-4 py-3 rounded-lg border text-xs shadow-xl backdrop-blur transition-all duration-300 transform translate-y-1 ${bg}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

function getStatusBadgeClass(status) {
  if (status === 'VERIFIED' || status === 'APPROVED' || status === 'Completed' || status === 'On Track') return 'badge-verified';
  if (status === 'VERIFIED_WITH_WARNING' || status === 'Requires Attention') return 'badge-warning';
  if (status === 'CONTRADICTION_DETECTED' || status === 'UNSUPPORTED' || status === 'Behind Schedule') return 'badge-danger';
  return 'badge-info';
}
