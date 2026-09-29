// static/js/app.js - Application Lifecycle & Tab Router
document.addEventListener('DOMContentLoaded', async () => {
  setupNavigation();
  setupRoleSwitcher();
  await loadCoreData();
  switchTab('dashboard');
});

function setupNavigation() {
  document.querySelectorAll('[data-tab]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const tab = e.currentTarget.getAttribute('data-tab');
      switchTab(tab);
    });
  });
}

function setupRoleSwitcher() {
  const switcher = document.getElementById('role-switcher');
  if (!switcher) return;
  switcher.addEventListener('change', (e) => {
    state.currentRole = e.target.value;
    showToast(`Active perspective changed to: ${state.currentRole.toUpperCase()}`, 'info');
    if (state.currentRole.startsWith('emp')) {
      switchTab('employee-portal');
    }
  });
}

function switchTab(tabName) {
  state.currentTab = tabName;
  document.querySelectorAll('[data-tab]').forEach(btn => {
    if (btn.getAttribute('data-tab') === tabName) {
      btn.classList.add('bg-blue-600', 'text-white');
      btn.classList.remove('text-slate-400', 'hover:bg-slate-800');
    } else {
      btn.classList.remove('bg-blue-600', 'text-white');
      btn.classList.add('text-slate-400', 'hover:bg-slate-800');
    }
  });

  document.querySelectorAll('.tab-view').forEach(view => view.classList.add('hidden'));
  const targetView = document.getElementById(`view-${tabName}`);
  if (targetView) targetView.classList.remove('hidden');

  if (tabName === 'dashboard') renderDashboard();
  if (tabName === 'documents') renderDocuments();
  if (tabName === 'role-matrix') renderRoleMatrix();
  if (tabName === 'onboarding') renderOnboarding();
  if (tabName === 'validation') renderValidation();
  if (tabName === 'reviews') renderReviewQueue();
  if (tabName === 'employee-portal') renderEmployeePortal();
  if (tabName === 'policy-impact') renderPolicyImpact();
  if (tabName === 'reports') renderReports();
}

async function loadCoreData() {
  try {
    state.employees = await fetchAPI('/employees');
    state.roles = await fetchAPI('/roles');
    state.documents = await fetchAPI('/documents');
    populateEmployeeDropdowns();
  } catch (e) {
    console.error('Initialization error:', e);
  }
}

function populateEmployeeDropdowns() {
  const selects = ['onboarding-emp-select', 'portal-emp-select'];
  selects.forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = state.employees.map(e => 
      `<option value="${e.id}">${e.employee_code} — ${e.full_name} (${e.role})</option>`
    ).join('');
    el.value = state.selectedEmployeeId;
    el.addEventListener('change', (ev) => {
      state.selectedEmployeeId = parseInt(ev.target.value);
      if (state.currentTab === 'onboarding') renderOnboarding();
      if (state.currentTab === 'employee-portal') renderEmployeePortal();
    });
  });
}
