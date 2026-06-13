/* ===========================
   Reservation Form Logic
   =========================== */

(function() {
  const form = document.getElementById('reservationForm');
  if (!form) return;

  // Live summary update
  const fields = {
    guestName:  'sum-name',
    guestPhone: 'sum-phone',
    guestEmail: 'sum-email',
    resDate:    'sum-date',
    resTime:    'sum-time',
    guestCount: 'sum-guests',
  };

  function updateSummary() {
    Object.entries(fields).forEach(([fieldId, sumId]) => {
      const input = document.getElementById(fieldId);
      const sumEl = document.getElementById(sumId);
      if (!input || !sumEl) return;

      const val = input.value.trim();
      if (val) {
        let display = val;
        if (fieldId === 'resDate') {
          display = formatDate(val);
        } else if (fieldId === 'guestCount') {
          display = val + (val === '1' ? ' Kişi' : ' Kişi');
        }
        sumEl.textContent = display;
        sumEl.classList.remove('empty');
      } else {
        sumEl.textContent = '—';
        sumEl.classList.add('empty');
      }
    });

    // Table preference
    const tableRadio = document.querySelector('input[name="tablePreference"]:checked');
    const sumTable = document.getElementById('sum-table');
    if (tableRadio && sumTable) {
      const labels = { window: 'Pencere Kenarı', private: 'Özel Köşe', any: 'Şef Seçimi' };
      sumTable.textContent = labels[tableRadio.value] || 'Şef Seçimi';
      sumTable.classList.remove('empty');
    }
  }

  function formatDate(dateStr) {
    if (!dateStr) return '';
    const [y, m, d] = dateStr.split('-');
    const months = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];
    const days = ['Pazar','Pazartesi','Salı','Çarşamba','Perşembe','Cuma','Cumartesi'];
    const date = new Date(dateStr);
    return `${d} ${months[parseInt(m)-1]} ${y}, ${days[date.getDay()]}`;
  }

  // Attach live update listeners
  form.querySelectorAll('input, select, textarea').forEach(el => {
    el.addEventListener('input', updateSummary);
    el.addEventListener('change', updateSummary);
  });

  // Validation
  function validate() {
    let valid = true;

    const rules = [
      { id: 'guestName',  check: v => v.trim().length >= 2,      errId: 'err-guestName',  msg: 'Ad soyad en az 2 karakter olmalıdır.' },
      { id: 'guestPhone', check: v => /^[\d\s\+\-\(\)]{7,}$/.test(v.trim()), errId: 'err-guestPhone', msg: 'Geçerli bir telefon numarası girin.' },
      { id: 'guestEmail', check: v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()), errId: 'err-guestEmail', msg: 'Geçerli bir e-posta adresi girin.' },
      { id: 'resDate',    check: v => v !== '',                   errId: 'err-resDate',    msg: 'Lütfen bir tarih seçin.' },
      { id: 'resTime',    check: v => v !== '',                   errId: 'err-resTime',    msg: 'Lütfen bir saat seçin.' },
      { id: 'guestCount', check: v => v !== '',                   errId: 'err-guestCount', msg: 'Kişi sayısı seçin.' },
    ];

    rules.forEach(rule => {
      const input = document.getElementById(rule.id);
      const errEl = document.getElementById(rule.errId);
      if (!input || !errEl) return;

      const val = input.value;
      if (!rule.check(val)) {
        input.classList.add('error');
        errEl.textContent = rule.msg;
        errEl.classList.add('show');
        valid = false;
      } else {
        input.classList.remove('error');
        errEl.classList.remove('show');
      }
    });

    // Date must be in the future
    const dateInput = document.getElementById('resDate');
    const errDate = document.getElementById('err-resDate');
    if (dateInput && dateInput.value) {
      const selected = new Date(dateInput.value);
      const today = new Date();
      today.setHours(0,0,0,0);
      if (selected < today) {
        dateInput.classList.add('error');
        errDate.textContent = 'Geçmiş tarih seçilemez.';
        errDate.classList.add('show');
        valid = false;
      }
    }

    return valid;
  }

  // Clear errors on input
  form.querySelectorAll('input, select').forEach(el => {
    el.addEventListener('input', function() {
      this.classList.remove('error');
      const errEl = document.getElementById('err-' + this.id);
      if (errEl) errEl.classList.remove('show');
    });
  });

  // Generate reservation code
  function generateCode() {
    const num = Math.floor(100000 + Math.random() * 900000);
    return 'EDO-' + num;
  }

  // Save to localStorage
  function saveReservation(data) {
    const existing = JSON.parse(localStorage.getItem('letoile_reservations') || '[]');
    existing.unshift(data);
    localStorage.setItem('letoile_reservations', JSON.stringify(existing));
  }

  // Update step indicators
  function setStep(step) {
    for (let i = 1; i <= 4; i++) {
      const stepEl = document.getElementById('step-' + i);
      if (!stepEl) continue;
      stepEl.classList.remove('active', 'done');
      if (i < step) stepEl.classList.add('done');
      else if (i === step) stepEl.classList.add('active');
    }
    for (let i = 1; i <= 3; i++) {
      const conn = document.getElementById('connector-' + i);
      if (!conn) continue;
      if (i < step) conn.classList.add('done');
      else conn.classList.remove('done');
    }
  }

  // Form submit
  form.addEventListener('submit', function(e) {
    e.preventDefault();

    if (!validate()) {
      // Scroll to first error
      const firstErr = form.querySelector('.error');
      if (firstErr) firstErr.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }

    const btn = document.getElementById('submitBtn');
    btn.textContent = 'İşleniyor...';
    btn.disabled = true;

    const code = generateCode();
    const tableLabels = { window: 'Pencere Kenarı', private: 'Özel Köşe', any: 'Şef Seçimi' };
    const tableRadio = document.querySelector('input[name="tablePreference"]:checked');
    const tablePref = tableRadio ? (tableLabels[tableRadio.value] || 'Şef Seçimi') : 'Şef Seçimi';

    const formData = {
      id: code,
      name: document.getElementById('guestName').value.trim(),
      phone: document.getElementById('guestPhone').value.trim(),
      email: document.getElementById('guestEmail').value.trim(),
      date: document.getElementById('resDate').value,
      time: document.getElementById('resTime').value,
      guests: document.getElementById('guestCount').value,
      tablePreference: tablePref,
      occasion: document.getElementById('occasion').value || '',
      note: document.getElementById('specialNote').value.trim(),
      status: 'pending',
      createdAt: new Date().toISOString(),
    };

    // Simulate short delay for effect
    setTimeout(() => {
      saveReservation(formData);
      showConfirmation(formData, code);
      setStep(4);
    }, 800);
  });

  function showConfirmation(data, code) {
    // Hide form
    document.getElementById('form-step-1').style.display = 'none';

    // Show confirmation
    const screen = document.getElementById('confirmationScreen');
    screen.classList.add('show');

    // Set code
    document.getElementById('confirmCode').textContent = code;

    // Build details
    const months = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];
    const [y, m, d] = data.date.split('-');
    const dateFormatted = `${d} ${months[parseInt(m)-1]} ${y}`;
    const occasionLabels = {
      birthday: '🎂 Doğum Günü', anniversary: '💍 Yıl Dönümü',
      proposal: '💍 Evlilik Teklifi', business: '💼 İş Yemeği',
      family: '👨‍👩‍👧 Aile Yemeği', romantic: '❤️ Romantik Akşam', other: 'Diğer'
    };

    const details = [
      { label: 'Misafir', value: data.name },
      { label: 'Tarih', value: dateFormatted },
      { label: 'Saat', value: data.time },
      { label: 'Kişi Sayısı', value: data.guests + ' Kişi' },
      { label: 'Masa Tercihi', value: data.tablePreference },
      { label: 'Durum', value: '⏳ Onay Bekliyor' },
    ];
    if (data.occasion) details.push({ label: 'Özel Durum', value: occasionLabels[data.occasion] || data.occasion });

    const detailsHtml = details.map(d =>
      `<div class="confirmation-detail-row"><span>${d.label}</span><span>${d.value}</span></div>`
    ).join('');
    document.getElementById('confirmDetails').innerHTML = detailsHtml;

    // Scroll to top of confirmation
    screen.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // Initial update
  updateSummary();
})();
