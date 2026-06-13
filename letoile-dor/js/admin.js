/* ===========================
   Admin Panel Logic
   =========================== */

// Auth
const ADMIN_USER = 'admin';
const ADMIN_PASS = 'admin123';
const STORAGE_KEY = 'letoile_reservations';
const SESSION_KEY = 'letoile_admin_session';

let currentPage = 'dashboard';
let allReservations = [];
let filteredReservations = [];
let currentSort = { field: 'date', dir: 'desc' };
let currentModalRes = null;
const PAGE_SIZE = 10;
let currentPageNum = 1;

// Table data
const TABLES = [
  { id: 1, name: 'Masa 1', capacity: 2, type: 'Pencere', status: 'available' },
  { id: 2, name: 'Masa 2', capacity: 4, type: 'Merkez', status: 'reserved' },
  { id: 3, name: 'Masa 3', capacity: 2, type: 'Köşe', status: 'occupied' },
  { id: 4, name: 'Masa 4', capacity: 6, type: 'Özel Salon', status: 'available' },
  { id: 5, name: 'Masa 5', capacity: 4, type: 'Pencere', status: 'reserved' },
  { id: 6, name: 'Masa 6', capacity: 8, type: 'Büyük Salon', status: 'available' },
  { id: 7, name: 'Masa 7', capacity: 2, type: 'Bar Yanı', status: 'occupied' },
  { id: 8, name: 'Masa 8', capacity: 4, type: 'Teras', status: 'available' },
  { id: 9, name: 'Masa 9', capacity: 6, type: 'Bahçe', status: 'reserved' },
  { id: 10, name: 'Masa 10', capacity: 10, type: 'VIP Salon', status: 'available' },
  { id: 11, name: 'Masa 11', capacity: 2, type: 'Merkez', status: 'available' },
  { id: 12, name: 'Masa 12', capacity: 4, type: 'Köşe', status: 'available' },
];

// ─── Init ──────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function() {
  // Check session
  if (localStorage.getItem(SESSION_KEY) === 'true') {
    showAdmin();
  }

  // Set date in topbar
  const topbarDate = document.getElementById('topbarDate');
  if (topbarDate) {
    const now = new Date();
    topbarDate.textContent = now.toLocaleDateString('tr-TR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
  }

  // Login form
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const user = document.getElementById('loginUser').value.trim();
      const pass = document.getElementById('loginPass').value;
      if (user === ADMIN_USER && pass === ADMIN_PASS) {
        localStorage.setItem(SESSION_KEY, 'true');
        showAdmin();
      } else {
        document.getElementById('loginError').classList.add('show');
      }
    });
  }

  // Logout
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', function() {
      localStorage.removeItem(SESSION_KEY);
      document.getElementById('adminWrapper').classList.remove('show');
      document.getElementById('loginScreen').style.display = 'flex';
    });
  }

  // Sidebar nav
  document.querySelectorAll('.sidebar-link[data-page]').forEach(link => {
    link.addEventListener('click', function() {
      showPage(this.dataset.page);
    });
  });

  // Sidebar toggle (mobile)
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('adminSidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function() {
      sidebar.classList.toggle('open');
    });
    document.addEventListener('click', function(e) {
      if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    });
  }

  // Seed demo data if empty
  seedDemoData();
});

function showAdmin() {
  document.getElementById('loginScreen').style.display = 'none';
  document.getElementById('adminWrapper').classList.add('show');
  loadReservations();
  renderDashboard();
  renderTables();
}

// ─── Data ──────────────────────────────────────────────────────────────────

function loadReservations() {
  allReservations = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  filteredReservations = [...allReservations];
  updatePendingBadge();
}

function updatePendingBadge() {
  const badge = document.getElementById('pendingBadge');
  if (!badge) return;
  const count = allReservations.filter(r => r.status === 'pending').length;
  badge.textContent = count;
  badge.style.display = count > 0 ? 'inline' : 'none';
}

function saveReservations() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(allReservations));
  updatePendingBadge();
}

function seedDemoData() {
  const existing = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  if (existing.length > 0) return;

  const today = new Date();
  const demo = [
    { id: 'EDO-001234', name: 'Ahmet Yılmaz', phone: '+90 532 111 22 33', email: 'ahmet@example.com', date: formatISO(0), time: '19:30', guests: '2', tablePreference: 'Pencere Kenarı', occasion: 'anniversary', note: 'Yıl dönümümüz, sürpriz hazırlık yapılabilir mi?', status: 'confirmed', createdAt: new Date().toISOString() },
    { id: 'EDO-002345', name: 'Selin Demir', phone: '+90 542 222 33 44', email: 'selin@example.com', date: formatISO(0), time: '21:00', guests: '4', tablePreference: 'Şef Seçimi', occasion: 'business', note: '', status: 'pending', createdAt: new Date().toISOString() },
    { id: 'EDO-003456', name: 'Mehmet Kaya', phone: '+90 555 333 44 55', email: 'mehmet@example.com', date: formatISO(1), time: '20:00', guests: '6', tablePreference: 'Özel Köşe', occasion: 'birthday', note: 'Doğum günü pastası istenebilir.', status: 'pending', createdAt: new Date().toISOString() },
    { id: 'EDO-004567', name: 'Ayşe Çelik', phone: '+90 505 444 55 66', email: 'ayse@example.com', date: formatISO(2), time: '18:30', guests: '2', tablePreference: 'Pencere Kenarı', occasion: 'romantic', note: '', status: 'confirmed', createdAt: new Date().toISOString() },
    { id: 'EDO-005678', name: 'Can Öztürk', phone: '+90 532 555 66 77', email: 'can@example.com', date: formatISO(-1), time: '19:00', guests: '3', tablePreference: 'Şef Seçimi', occasion: '', note: 'Gluten alerjim var.', status: 'completed', createdAt: new Date(Date.now() - 86400000).toISOString() },
    { id: 'EDO-006789', name: 'Zeynep Arslan', phone: '+90 542 666 77 88', email: 'zeynep@example.com', date: formatISO(-2), time: '20:30', guests: '5', tablePreference: 'Özel Köşe', occasion: 'family', note: '', status: 'cancelled', createdAt: new Date(Date.now() - 172800000).toISOString() },
  ];
  localStorage.setItem(STORAGE_KEY, JSON.stringify(demo));
}

function formatISO(daysOffset) {
  const d = new Date();
  d.setDate(d.getDate() + daysOffset);
  return d.toISOString().split('T')[0];
}

// ─── Dashboard ─────────────────────────────────────────────────────────────

function renderDashboard() {
  loadReservations();
  const today = new Date().toISOString().split('T')[0];

  const total = allReservations.length;
  const todayRes = allReservations.filter(r => r.date === today).length;
  const confirmed = allReservations.filter(r => r.status === 'confirmed').length;
  const cancelled = allReservations.filter(r => r.status === 'cancelled').length;

  setText('stat-total', total);
  setText('stat-today', todayRes);
  setText('stat-confirmed', confirmed);
  setText('stat-cancelled', cancelled);

  // Dashboard table (last 5)
  const tbody = document.getElementById('dashboardTableBody');
  if (!tbody) return;

  const recent = allReservations.slice(0, 5);
  if (recent.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5"><div class="table-empty"><div class="table-empty-icon">📋</div><p>Henüz rezervasyon bulunmuyor.</p></div></td></tr>`;
    return;
  }
  tbody.innerHTML = recent.map(r => `
    <tr>
      <td>
        <div class="res-name">${escHtml(r.name)}</div>
        <div class="res-contact">${escHtml(r.email)}</div>
      </td>
      <td>
        <div>${formatDateDisplay(r.date)}</div>
        <div style="color:var(--text-muted);font-size:0.78rem">${r.time}</div>
      </td>
      <td>${r.guests} Kişi</td>
      <td><span class="status-badge ${r.status}">${statusLabel(r.status)}</span></td>
      <td>
        <div class="action-menu">
          <button class="action-btn view" onclick="openModal('${r.id}')" title="Detay">👁</button>
          <button class="action-btn confirm" onclick="changeStatus('${r.id}','confirmed')" title="Onayla">✓</button>
          <button class="action-btn cancel" onclick="changeStatus('${r.id}','cancelled')" title="İptal">✕</button>
        </div>
      </td>
    </tr>
  `).join('');
}

// ─── Reservations Table ────────────────────────────────────────────────────

function renderReservationsTable() {
  const tbody = document.getElementById('reservationsTableBody');
  if (!tbody) return;

  const start = (currentPageNum - 1) * PAGE_SIZE;
  const pageItems = filteredReservations.slice(start, start + PAGE_SIZE);

  if (filteredReservations.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7"><div class="table-empty"><div class="table-empty-icon">🔍</div><p>Filtre kriterlerine uygun rezervasyon bulunamadı.</p></div></td></tr>`;
    renderPagination(0);
    return;
  }

  tbody.innerHTML = pageItems.map(r => `
    <tr>
      <td>
        <div class="res-id">${r.id}</div>
      </td>
      <td>
        <div class="res-name">${escHtml(r.name)}</div>
        <div class="res-contact">${escHtml(r.phone)}</div>
        <div class="res-contact">${escHtml(r.email)}</div>
      </td>
      <td>
        <div>${formatDateDisplay(r.date)}</div>
        <div style="color:var(--text-muted);font-size:0.78rem">${r.time}</div>
      </td>
      <td>${r.guests} Kişi</td>
      <td style="font-size:0.8rem;color:var(--text-muted)">${r.tablePreference || '—'}</td>
      <td><span class="status-badge ${r.status}">${statusLabel(r.status)}</span></td>
      <td>
        <div class="action-menu">
          <button class="action-btn view" onclick="openModal('${r.id}')" title="Detay">👁</button>
          <button class="action-btn confirm" onclick="changeStatus('${r.id}','confirmed')" title="Onayla">✓</button>
          <button class="action-btn cancel" onclick="changeStatus('${r.id}','cancelled')" title="İptal">✕</button>
          <button class="action-btn delete" onclick="deleteReservation('${r.id}')" title="Sil">🗑</button>
        </div>
      </td>
    </tr>
  `).join('');

  renderPagination(filteredReservations.length);
  setText('paginationInfo', `${filteredReservations.length} rezervasyon (${start+1}–${Math.min(start+PAGE_SIZE, filteredReservations.length)} gösteriliyor)`);
}

function renderPagination(total) {
  const container = document.getElementById('paginationBtns');
  if (!container) return;
  const pages = Math.ceil(total / PAGE_SIZE);
  if (pages <= 1) { container.innerHTML = ''; return; }

  let html = `<button class="page-btn" onclick="goPage(${currentPageNum-1})" ${currentPageNum===1?'disabled':''}>‹</button>`;
  for (let i = 1; i <= pages; i++) {
    html += `<button class="page-btn ${i===currentPageNum?'active':''}" onclick="goPage(${i})">${i}</button>`;
  }
  html += `<button class="page-btn" onclick="goPage(${currentPageNum+1})" ${currentPageNum===pages?'disabled':''}>›</button>`;
  container.innerHTML = html;
}

function goPage(p) {
  const pages = Math.ceil(filteredReservations.length / PAGE_SIZE);
  if (p < 1 || p > pages) return;
  currentPageNum = p;
  renderReservationsTable();
}

// ─── Filters ───────────────────────────────────────────────────────────────

function applyFilters() {
  const search = (document.getElementById('searchInput')?.value || '').toLowerCase();
  const date = document.getElementById('filterDate')?.value || '';
  const time = document.getElementById('filterTime')?.value || '';
  const guests = document.getElementById('filterGuests')?.value || '';
  const status = document.getElementById('filterStatus')?.value || '';

  filteredReservations = allReservations.filter(r => {
    if (search && !(
      r.name.toLowerCase().includes(search) ||
      r.email.toLowerCase().includes(search) ||
      r.phone.includes(search) ||
      r.id.toLowerCase().includes(search)
    )) return false;
    if (date && r.date !== date) return false;
    if (time) {
      const hour = parseInt(r.time.split(':')[0]);
      if (time === '12' && !(hour >= 12 && hour < 14)) return false;
      if (time === '18' && !(hour >= 18 && hour < 20)) return false;
      if (time === '20' && !(hour >= 20)) return false;
    }
    if (guests) {
      const g = parseInt(r.guests);
      if (guests === '1-2' && !(g >= 1 && g <= 2)) return false;
      if (guests === '3-4' && !(g >= 3 && g <= 4)) return false;
      if (guests === '5+' && g < 5) return false;
    }
    if (status && r.status !== status) return false;
    return true;
  });

  currentPageNum = 1;
  renderReservationsTable();
}

function clearFilters() {
  ['searchInput','filterDate','filterTime','filterGuests','filterStatus'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
  filteredReservations = [...allReservations];
  currentPageNum = 1;
  renderReservationsTable();
}

// ─── Sort ──────────────────────────────────────────────────────────────────

function sortTable(field) {
  if (currentSort.field === field) {
    currentSort.dir = currentSort.dir === 'asc' ? 'desc' : 'asc';
  } else {
    currentSort.field = field;
    currentSort.dir = 'asc';
  }
  const dir = currentSort.dir === 'asc' ? 1 : -1;
  filteredReservations.sort((a, b) => {
    const va = (a[field] || '').toString().toLowerCase();
    const vb = (b[field] || '').toString().toLowerCase();
    return va < vb ? -dir : va > vb ? dir : 0;
  });
  renderReservationsTable();
}

// ─── Status & Actions ──────────────────────────────────────────────────────

function changeStatus(id, status) {
  const idx = allReservations.findIndex(r => r.id === id);
  if (idx === -1) return;
  allReservations[idx].status = status;
  saveReservations();
  loadReservations();
  applyFilters();
  if (currentPage === 'dashboard') renderDashboard();
  if (currentModalRes && currentModalRes.id === id) {
    currentModalRes.status = status;
    openModal(id);
  }
}

function deleteReservation(id) {
  if (!confirm('Bu rezervasyonu silmek istediğinizden emin misiniz?')) return;
  allReservations = allReservations.filter(r => r.id !== id);
  saveReservations();
  loadReservations();
  applyFilters();
  renderDashboard();
  closeModal();
}

// ─── Modal ─────────────────────────────────────────────────────────────────

function openModal(id) {
  const res = allReservations.find(r => r.id === id);
  if (!res) return;
  currentModalRes = res;

  const occasionLabels = {
    birthday: '🎂 Doğum Günü', anniversary: '💍 Yıl Dönümü',
    proposal: '💍 Evlilik Teklifi', business: '💼 İş Yemeği',
    family: '👨‍👩‍👧 Aile Yemeği', romantic: '❤️ Romantik Akşam', other: 'Diğer'
  };

  const rows = [
    { label: 'Rezervasyon No', value: `<code style="color:var(--gold)">${res.id}</code>` },
    { label: 'Ad Soyad', value: escHtml(res.name) },
    { label: 'Telefon', value: `<a href="tel:${res.phone}" style="color:var(--gold)">${escHtml(res.phone)}</a>` },
    { label: 'E-posta', value: `<a href="mailto:${res.email}" style="color:var(--gold)">${escHtml(res.email)}</a>` },
    { label: 'Tarih', value: formatDateDisplay(res.date) },
    { label: 'Saat', value: res.time },
    { label: 'Kişi Sayısı', value: res.guests + ' Kişi' },
    { label: 'Masa Tercihi', value: res.tablePreference || '—' },
    { label: 'Özel Durum', value: occasionLabels[res.occasion] || (res.occasion ? res.occasion : '—') },
    { label: 'Not', value: res.note ? `<em style="color:var(--beige)">${escHtml(res.note)}</em>` : '—' },
    { label: 'Mevcut Durum', value: `<span class="status-badge ${res.status}">${statusLabel(res.status)}</span>` },
    { label: 'Oluşturulma', value: new Date(res.createdAt).toLocaleString('tr-TR') },
  ];

  const html = `
    ${rows.map(r => `<div class="detail-row"><span class="detail-label">${r.label}</span><span class="detail-value">${r.value}</span></div>`).join('')}
    <div class="status-change-wrap">
      <div class="status-change-title">Durum Değiştir</div>
      <div class="status-btns">
        <button class="status-action-btn pending" onclick="changeStatus('${res.id}','pending')">⏳ Beklemede</button>
        <button class="status-action-btn confirm" onclick="changeStatus('${res.id}','confirmed')">✓ Onayla</button>
        <button class="status-action-btn cancel" onclick="changeStatus('${res.id}','cancelled')">✕ İptal Et</button>
        <button class="status-action-btn complete" onclick="changeStatus('${res.id}','completed')">★ Tamamlandı</button>
      </div>
    </div>
    <div style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid var(--glass-border)">
      <button class="btn btn-ghost" style="font-size:0.72rem" onclick="deleteReservation('${res.id}')">🗑 Rezervasyonu Sil</button>
    </div>
  `;

  document.getElementById('modalBody').innerHTML = html;
  document.getElementById('detailModal').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  document.getElementById('detailModal').classList.remove('open');
  document.body.style.overflow = '';
  currentModalRes = null;
}

document.getElementById('detailModal')?.addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});

// ─── Tables ────────────────────────────────────────────────────────────────

function renderTables() {
  const grid = document.getElementById('tablesGrid');
  if (!grid) return;
  const icons = { available: '🟢', occupied: '🔴', reserved: '🟡' };
  const labels = { available: 'Boş', occupied: 'Dolu', reserved: 'Rezerveli' };
  grid.innerHTML = TABLES.map(t => `
    <div class="table-card-admin ${t.status}">
      <div class="tc-icon">${icons[t.status]}</div>
      <div class="tc-num">${t.name}</div>
      <div class="tc-info">${t.capacity} Kişilik · ${t.type}</div>
      <span class="tc-status ${t.status}">${labels[t.status]}</span>
    </div>
  `).join('');
}

// ─── Page Navigation ───────────────────────────────────────────────────────

function showPage(page) {
  currentPage = page;

  // Update sidebar
  document.querySelectorAll('.sidebar-link[data-page]').forEach(l => {
    l.classList.toggle('active', l.dataset.page === page);
  });

  // Hide all pages
  ['dashboard','reservations','tables'].forEach(p => {
    const el = document.getElementById('page-' + p);
    if (el) el.style.display = 'none';
  });

  // Show target
  const target = document.getElementById('page-' + page);
  if (target) target.style.display = 'block';

  // Update topbar
  const titles = { dashboard: 'Gösterge Paneli', reservations: 'Rezervasyonlar', tables: 'Masa Yönetimi' };
  const subs = { dashboard: 'Günlük özet ve son aktiviteler', reservations: 'Tüm rezervasyonları görüntüleyin ve yönetin', tables: 'Masa durumlarını takip edin' };
  setText('topbarTitle', titles[page] || '');
  setText('topbarSub', subs[page] || '');

  // Page-specific init
  if (page === 'dashboard') {
    renderDashboard();
  } else if (page === 'reservations') {
    loadReservations();
    filteredReservations = [...allReservations];
    renderReservationsTable();
  } else if (page === 'tables') {
    renderTables();
  }

  // Close mobile sidebar
  document.getElementById('adminSidebar')?.classList.remove('open');
}

// ─── Export CSV ────────────────────────────────────────────────────────────

function exportCSV() {
  const headers = ['ID','Ad Soyad','Telefon','E-posta','Tarih','Saat','Kişi','Masa','Özel Durum','Not','Durum','Oluşturulma'];
  const rows = filteredReservations.map(r => [
    r.id, r.name, r.phone, r.email, r.date, r.time, r.guests,
    r.tablePreference, r.occasion || '', r.note || '', statusLabel(r.status),
    new Date(r.createdAt).toLocaleString('tr-TR')
  ].map(v => `"${(v+'').replace(/"/g,'""')}"`).join(','));

  const csv = [headers.join(','), ...rows].join('\n');
  const blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `letoile-rezervasyonlar-${new Date().toISOString().split('T')[0]}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

// ─── Helpers ───────────────────────────────────────────────────────────────

function setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

function escHtml(str) {
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function formatDateDisplay(dateStr) {
  if (!dateStr) return '—';
  const months = ['Oca','Şub','Mar','Nis','May','Haz','Tem','Ağu','Eyl','Eki','Kas','Ara'];
  const [y, m, d] = dateStr.split('-');
  return `${d} ${months[parseInt(m)-1]} ${y}`;
}

function statusLabel(status) {
  const labels = { pending: 'Beklemede', confirmed: 'Onaylandı', cancelled: 'İptal Edildi', completed: 'Tamamlandı' };
  return labels[status] || status;
}
