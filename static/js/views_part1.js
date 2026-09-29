// static/js/views_part1.js - Core Views: Dashboard, Documents, Role Matrix, Onboarding

async function renderDashboard() {
  const report = await fetchAPI('/reports/compliance');
  state.complianceReport = report;
  
  const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };
  setEl('stat-total-docs', state.documents.length);
  setEl('stat-total-roles', state.roles.length);
  setEl('stat-total-emps', report.summary.total_employees);
  setEl('stat-avg-coverage', `${report.summary.average_mandatory_coverage}%`);
  setEl('stat-avg-traceability', `${report.summary.average_source_traceability}%`);
  setEl('stat-flagged-plans', report.summary.flagged_plans_requiring_review);

  const tbody = document.getElementById('dashboard-recent-table');
  if (tbody) {
    tbody.innerHTML = report.recent_plans.map(p => `
      <tr class="border-b border-slate-800/80 hover:bg-slate-800/30">
        <td class="py-3 px-4 font-mono font-bold text-sky-400">#PLAN-${p.plan_id}</td>
        <td class="py-3 px-4 font-medium text-slate-200">${p.employee}</td>
        <td class="py-3 px-4 text-xs text-slate-400">${p.role}</td>
        <td class="py-3 px-4">
          <span class="px-2.5 py-0.5 text-xs font-bold rounded-full ${getStatusBadgeClass(p.status)}">
            ${p.status}
          </span>
        </td>
        <td class="py-3 px-4 font-bold text-emerald-400">${p.coverage_score}%</td>
        <td class="py-3 px-4 font-bold text-sky-400">${p.traceability_score}%</td>
        <td class="py-3 px-4 text-right">
          <button onclick="viewPlanDetails(${p.plan_id})" class="px-2.5 py-1 bg-slate-800 hover:bg-blue-600 text-xs text-slate-200 rounded transition">Inspect</button>
        </td>
      </tr>
    `).join('') || `<tr><td colspan="7" class="py-4 text-center text-slate-500 text-xs">No active plans yet. Click 'Generate Onboarding' to begin.</td></tr>`;
  }
}

async function renderDocuments() {
  state.documents = await fetchAPI('/documents');
  const grid = document.getElementById('documents-grid');
  if (!grid) return;
  grid.innerHTML = state.documents.map(d => `
    <div class="glass-card rounded-xl p-5 relative overflow-hidden flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-sky-400">${d.doc_code}</span>
          <div class="flex items-center gap-1.5">
            <span class="text-xs px-2 py-0.5 rounded bg-blue-900/40 text-blue-300 font-semibold border border-blue-500/20">v${d.current_version}</span>
            <span class="text-xs px-2 py-0.5 rounded uppercase font-bold text-slate-400 bg-slate-800">${d.file_format}</span>
          </div>
        </div>
        <h4 class="text-base font-semibold text-slate-100 mb-2 leading-tight">${d.title}</h4>
        <p class="text-xs text-slate-400 mb-4">Department: <span class="text-slate-200 font-medium">${d.department}</span></p>
      </div>

      <div>
        <div class="flex items-center justify-between text-xs text-slate-400 pt-3 border-t border-slate-800">
          <span>Traceable Chunks: <strong class="text-slate-200">${d.chunks_count}</strong></span>
          <span>Precedence: <strong class="text-amber-400">Rank ${d.precedence_level}</strong></span>
        </div>
        ${d.is_flagged_adversarial ? `
          <div class="mt-2 text-xs py-1 px-2 bg-red-950/60 border border-red-500/40 text-red-300 rounded flex items-center gap-1">
            <span>⚠ Adversarial Injection Flagged</span>
          </div>` : ''}
        <button onclick="viewDocumentChunks(${d.id}, '${d.doc_code}')" class="w-full mt-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 rounded transition">
          Explore Chunks & Sections
        </button>
      </div>
    </div>
  `).join('');
}

async function viewDocumentChunks(docId, docCode) {
  const chunks = await fetchAPI(`/documents/${docId}/chunks`);
  const modal = document.getElementById('chunk-modal');
  const title = document.getElementById('chunk-modal-title');
  const body = document.getElementById('chunk-modal-body');
  if (!modal) return;
  title.innerText = `${docCode} — Traceable Chunks (${chunks.length} total)`;
  body.innerHTML = chunks.map(c => `
    <div class="p-3 bg-slate-900/80 rounded border border-slate-800 mb-3 text-xs">
      <div class="flex justify-between items-center mb-1 text-slate-400">
        <span class="font-bold text-sky-400 font-mono">Chunk #${c.chunk_index} | Section ${c.section_id}</span>
        <span>Page ${c.page_number} | ~${c.token_count} tokens</span>
      </div>
      <div class="font-semibold text-slate-200 mb-1">${c.section_heading}</div>
      <p class="text-slate-300 leading-relaxed">${c.content}</p>
    </div>
  `).join('') || '<p class="text-slate-400">No chunks available.</p>';
  modal.classList.remove('hidden');
}

async function renderRoleMatrix() {
  const overview = await fetchAPI('/role-matrix');
  const container = document.getElementById('role-matrix-container');
  if (!container) return;

  container.innerHTML = `
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
      ${overview.map(r => `
        <div class="glass-card p-5 rounded-xl flex flex-col justify-between">
          <div>
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs font-mono font-bold text-blue-400">${r.role_code}</span>
              <span class="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300">${r.experience_level}</span>
            </div>
            <h4 class="text-base font-bold text-slate-100 mb-1">${r.role_name}</h4>
            <p class="text-xs text-slate-400 mb-4">${r.department}</p>
          </div>
          <div>
            <div class="grid grid-cols-3 gap-2 py-3 border-t border-slate-800 text-center mb-3">
              <div class="bg-slate-900/60 p-2 rounded">
                <span class="text-[11px] text-slate-400 block">Total</span>
                <strong class="text-sm text-slate-100">${r.total_requirements}</strong>
              </div>
              <div class="bg-slate-900/60 p-2 rounded">
                <span class="text-[11px] text-slate-400 block">Mandatory</span>
                <strong class="text-sm text-emerald-400">${r.mandatory_count}</strong>
              </div>
              <div class="bg-slate-900/60 p-2 rounded">
                <span class="text-[11px] text-slate-400 block">Optional</span>
                <strong class="text-sm text-amber-400">${r.optional_count}</strong>
              </div>
            </div>
            <button onclick="viewRoleDetails(${r.role_id})" class="w-full py-2 bg-blue-600 hover:bg-blue-700 text-xs font-bold text-white rounded-lg transition">
              Inspect Role Matrix
            </button>
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

async function viewRoleDetails(roleId) {
  const data = await fetchAPI(`/role-matrix/${roleId}`);
  const modal = document.getElementById('role-detail-modal');
  const title = document.getElementById('role-modal-title');
  const body = document.getElementById('role-modal-body');
  if (!modal) return;

  title.innerText = `Role Requirement Matrix: ${data.role_name} (${data.role_code})`;
  body.innerHTML = `
    <div class="mb-4 text-xs text-slate-300 bg-slate-900 p-3 rounded border border-slate-800">
      <p class="mb-1"><strong>Department:</strong> ${data.department} | <strong>Level:</strong> ${data.experience_level} | <strong>Total Requirements:</strong> ${data.total_requirements}</p>
      <p><strong>Description:</strong> ${data.description}</p>
    </div>
    <div class="space-y-2 max-h-[500px] overflow-y-auto pr-1">
      ${data.mandatory_requirements.map(req => `
        <div class="p-3 bg-slate-900/90 rounded border-l-4 border-emerald-500 border-t border-r border-b border-slate-800 text-xs">
          <div class="flex justify-between items-center mb-1">
            <span class="font-mono font-bold text-emerald-400">${req.requirement_code} [${req.category}]</span>
            <span class="text-slate-400">Due: <strong class="text-slate-200">${req.due_stage}</strong> | Priority: <strong class="text-rose-400">${req.priority}</strong></span>
          </div>
          <p class="text-slate-200 font-medium mb-1.5">${req.text}</p>
          <div class="text-[11px] text-slate-400 flex items-center justify-between">
            <span>Competency: <strong class="text-sky-300">${req.competency}</strong></span>
            <span>Source: <strong class="text-amber-300">${req.document_code} §${req.section_id} (v${req.version})</strong></span>
          </div>
        </div>
      `).join('')}
    </div>
  `;
  modal.classList.remove('hidden');
}

async function renderOnboarding() {
  const empId = state.selectedEmployeeId;
  const emp = state.employees.find(e => e.id === empId);
  if (!emp) return;

  const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };
  setEl('plan-emp-name', emp.full_name);
  setEl('plan-emp-role', `${emp.role} (${emp.experience_level})`);
  setEl('plan-emp-dept', emp.department);

  try {
    const plan = await fetchAPI(`/onboarding/employee/${empId}`);
    state.activePlan = plan;
    state.selectedPlanId = plan.id;
    displayOnboardingPlan(plan);
  } catch (err) {
    document.getElementById('plan-display-area').innerHTML = `
      <div class="p-10 text-center glass-card rounded-xl">
        <h3 class="text-lg font-bold text-slate-200 mb-2">No Active Onboarding Journey Yet</h3>
        <p class="text-sm text-slate-400 mb-6">Click the button below to synthesize an AI-grounded, multi-stage personalized curriculum.</p>
        <button onclick="triggerGeneratePlan()" class="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-sm font-bold text-white rounded-lg shadow-lg shadow-blue-500/20 transition">
          ✨ Synthesize Personalized Onboarding Plan
        </button>
      </div>
    `;
  }
}

async function triggerGeneratePlan() {
  showToast('Synthesizing curriculum and executing Python Ground-Truth validator...', 'info');
  try {
    const res = await fetchAPI('/onboarding/generate', {
      method: 'POST',
      body: JSON.stringify({ employee_id: state.selectedEmployeeId })
    });
    showToast(`Plan synthesized successfully! Validation Status: ${res.status}`, 'success');
    renderOnboarding();
  } catch (err) {
    showToast(`Generation failed: ${err.message}`, 'error');
  }
}

function displayOnboardingPlan(plan) {
  const container = document.getElementById('plan-display-area');
  if (!container) return;

  container.innerHTML = `
    <div class="glass-panel p-6 rounded-xl mb-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
        <div>
          <div class="flex items-center gap-3 mb-1">
            <h3 class="text-xl font-bold text-slate-100">${plan.title}</h3>
            <span class="px-3 py-1 text-xs font-bold rounded-full ${getStatusBadgeClass(plan.status)}">${plan.status}</span>
          </div>
          <p class="text-xs text-slate-400">Employee: <strong class="text-slate-200">${plan.employee_name}</strong> | Role: <strong class="text-slate-200">${plan.role_name}</strong> | Model: <strong class="text-sky-400">${plan.model_used}</strong></p>
        </div>
        <div class="flex items-center gap-3">
          <button onclick="switchTab('validation')" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-lg border border-slate-700 transition">
            🔬 View Python Ground Truth Results
          </button>
          <button onclick="triggerGeneratePlan()" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-xs font-bold text-white rounded-lg transition">
            🔄 Regenerate Curriculum
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div class="glass-card p-4 rounded-lg flex items-center justify-between border-l-4 border-emerald-500">
          <div>
            <span class="text-xs text-slate-400 block">Mandatory Coverage Score</span>
            <strong class="text-2xl text-emerald-400 font-extrabold">${plan.coverage_score}%</strong>
          </div>
          <span class="text-xs px-2 py-1 rounded bg-emerald-950 text-emerald-300 font-mono">Formula Grounded</span>
        </div>
        <div class="glass-card p-4 rounded-lg flex items-center justify-between border-l-4 border-sky-500">
          <div>
            <span class="text-xs text-slate-400 block">Source Traceability Score</span>
            <strong class="text-2xl text-sky-400 font-extrabold">${plan.traceability_score}%</strong>
          </div>
          <span class="text-xs px-2 py-1 rounded bg-sky-950 text-sky-300 font-mono">Active Citations</span>
        </div>
        <div class="glass-card p-4 rounded-lg flex items-center justify-between border-l-4 border-purple-500">
          <div>
            <span class="text-xs text-slate-400 block">GenAI Consistency Score</span>
            <strong class="text-2xl text-purple-400 font-extrabold">${plan.consistency_score}%</strong>
          </div>
          <span class="text-xs px-2 py-1 rounded bg-purple-950 text-purple-300 font-mono">Sampled Runs</span>
        </div>
      </div>

      <div class="border-b border-slate-800 mb-6 flex gap-4 overflow-x-auto pb-2">
        ${['Day 1', 'Week 1', 'Week 2', 'First 30 Days', 'First 60 Days', 'First 90 Days'].map((stage, idx) => `
          <button onclick="filterCurriculumStage('${stage}')" class="stage-filter-btn px-4 py-1.5 text-xs font-bold rounded-lg ${idx === 0 ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-400 hover:text-slate-200'}" data-stage="${stage}">
            ${stage}
          </button>
        `).join('')}
      </div>

      <div id="stage-modules-container" class="space-y-4"></div>
    </div>
  `;

  filterCurriculumStage('Day 1');
}

function filterCurriculumStage(stageName) {
  document.querySelectorAll('.stage-filter-btn').forEach(btn => {
    if (btn.getAttribute('data-stage') === stageName) {
      btn.classList.add('bg-blue-600', 'text-white');
      btn.classList.remove('bg-slate-800', 'text-slate-400');
    } else {
      btn.classList.remove('bg-blue-600', 'text-white');
      btn.classList.add('bg-slate-800', 'text-slate-400');
    }
  });

  const container = document.getElementById('stage-modules-container');
  if (!container || !state.activePlan) return;

  const stageModules = state.activePlan.modules.filter(m => m.stage === stageName);
  if (stageModules.length === 0) {
    container.innerHTML = `<div class="p-6 text-center text-slate-500 text-xs">No learning modules assigned to ${stageName}.</div>`;
    return;
  }

  container.innerHTML = stageModules.map(m => `
    <div class="glass-card p-5 rounded-xl border border-slate-800">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 mb-3">
        <div class="flex items-center gap-2">
          <span class="text-xs font-mono font-bold text-sky-400 bg-slate-900 px-2.5 py-1 rounded">${m.module_code}</span>
          <span class="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-semibold uppercase">${m.category}</span>
          <span class="text-xs px-2 py-0.5 rounded bg-blue-900/40 text-blue-300">${m.difficulty}</span>
        </div>
        <div class="text-xs text-slate-400">
          Source: <strong class="text-amber-400 font-mono">${m.source_doc_id} §${m.source_section_id}</strong>
        </div>
      </div>
      <h4 class="text-base font-bold text-slate-100 mb-2">${m.title}</h4>
      <p class="text-xs text-slate-300 mb-4 leading-relaxed">${m.purpose}</p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs mb-4">
        <div class="bg-slate-900/60 p-3 rounded-lg">
          <span class="text-slate-400 font-semibold block mb-1">Learning Objectives:</span>
          <ul class="list-disc list-inside text-slate-300 space-y-1">
            ${m.learning_objectives.map(o => `<li>${o}</li>`).join('')}
          </ul>
        </div>
        <div class="bg-slate-900/60 p-3 rounded-lg">
          <span class="text-slate-400 font-semibold block mb-1">Key Concepts:</span>
          <div class="flex flex-wrap gap-1.5 mt-1">
            ${m.key_concepts.map(c => `<span class="px-2 py-0.5 bg-slate-800 text-slate-300 rounded font-mono text-[11px]">${c}</span>`).join('')}
          </div>
        </div>
      </div>

      <div class="flex items-center justify-between pt-3 border-t border-slate-800 text-xs">
        <span class="text-slate-400">Duration: <strong class="text-slate-200">${m.estimated_duration_mins} mins</strong></span>
        <div class="flex items-center gap-2">
          ${m.has_quiz ? `<button onclick="startQuizModal(${m.quiz_id})" class="px-3 py-1.5 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded transition">Take Knowledge Quiz</button>` : ''}
          <button onclick="markModuleComplete(${m.id})" class="px-3 py-1.5 ${m.status === 'COMPLETED' ? 'bg-emerald-600' : 'bg-slate-800 hover:bg-emerald-600'} text-white font-semibold rounded transition">
            ${m.status === 'COMPLETED' ? '✓ Completed' : 'Mark Complete'}
          </button>
        </div>
      </div>
    </div>
  `).join('');
}

async function markModuleComplete(modId) {
  await fetchAPI(`/modules/${modId}/complete`, { method: 'POST' });
  showToast('Module marked as completed!', 'success');
  renderOnboarding();
}

function viewPlanDetails(planId) {
  state.selectedPlanId = planId;
  switchTab('onboarding');
}
