/* Kadıköy Kahve Dükkânı: az JavaScript (ES module yok, file:// ile çalışır)
   1) Mobil menü  2) Menü sekmeleri  3) Aktif bağlantı  4) "Şimdi açık" göstergesi
   Yumuşak kaydırma CSS'te (scroll-behavior) ve reduced-motion'a saygılıdır. */
(function () {
  'use strict';

  document.documentElement.classList.add('js');

  /* DOLDUR: çalışma saatleri. 0 = Pazar ... 6 = Cumartesi.
     Biçim: [açılış, kapanış] "SS:DD". Kapalı gün için null. Gece yarısını aşanlar için kapanış < açılış yazın (ör. ['10:00','01:00']).
     Tüm günler null kaldığı sürece gösterge gizli kalır. */
  var SAATLER = {
    0: null, // Pazar
    1: null, // Pazartesi
    2: null, // Salı
    3: null, // Çarşamba
    4: null, // Perşembe
    5: null, // Cuma
    6: null  // Cumartesi
  };

  /* ---------- 1) Mobil menü ---------- */
  var dugme = document.querySelector('.nav__dugme');
  var liste = document.getElementById('nav-menu');
  var ikonAc = dugme && dugme.querySelector('.ikon--ac');
  var ikonKapat = dugme && dugme.querySelector('.ikon--kapat');

  function menuDurumu(ac) {
    dugme.setAttribute('aria-expanded', String(ac));
    dugme.setAttribute('aria-label', ac ? 'Menüyü kapat' : 'Menüyü aç');
    liste.classList.toggle('acik', ac);
    // SVG öğelerinde "hidden" IDL özelliği yok; özniteliği doğrudan yönet
    if (ac) { ikonAc.setAttribute('hidden', ''); ikonKapat.removeAttribute('hidden'); }
    else { ikonAc.removeAttribute('hidden'); ikonKapat.setAttribute('hidden', ''); }
  }

  if (dugme && liste) {
    dugme.addEventListener('click', function () {
      menuDurumu(dugme.getAttribute('aria-expanded') !== 'true');
    });
    liste.addEventListener('click', function (e) {
      if (e.target.closest('a')) { menuDurumu(false); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && dugme.getAttribute('aria-expanded') === 'true') {
        menuDurumu(false);
        dugme.focus();
      }
    });
    // Masaüstü genişliğine geçilirse paneli sıfırla
    window.matchMedia('(min-width: 900px)').addEventListener('change', function () { menuDurumu(false); });
  }

  /* ---------- 2) Menü sekmeleri (mobil; masaüstünde CSS hepsini gösterir) ---------- */
  var sekmeler = Array.prototype.slice.call(document.querySelectorAll('.sekmeler [role="tab"]'));

  function sekmeSec(sekme, odakla) {
    sekmeler.forEach(function (s) {
      var secili = s === sekme;
      s.setAttribute('aria-selected', String(secili));
      s.tabIndex = secili ? 0 : -1;
      document.getElementById(s.getAttribute('aria-controls')).hidden = !secili;
    });
    if (odakla) { sekme.focus(); }
  }

  if (sekmeler.length) {
    sekmeSec(sekmeler[0], false);
    sekmeler.forEach(function (s, i) {
      s.addEventListener('click', function () { sekmeSec(s, false); });
      s.addEventListener('keydown', function (e) {
        var yeni = null;
        if (e.key === 'ArrowRight') { yeni = sekmeler[(i + 1) % sekmeler.length]; }
        if (e.key === 'ArrowLeft') { yeni = sekmeler[(i - 1 + sekmeler.length) % sekmeler.length]; }
        if (e.key === 'Home') { yeni = sekmeler[0]; }
        if (e.key === 'End') { yeni = sekmeler[sekmeler.length - 1]; }
        if (yeni) { e.preventDefault(); sekmeSec(yeni, true); }
      });
    });
  }

  /* ---------- 3) Kaydırırken aktif bağlantı ---------- */
  var baglantilar = document.querySelectorAll('.nav__liste a');
  if ('IntersectionObserver' in window && baglantilar.length) {
    var gozlem = new IntersectionObserver(function (kayitlar) {
      kayitlar.forEach(function (k) {
        if (!k.isIntersecting) { return; }
        baglantilar.forEach(function (a) {
          if (a.getAttribute('href') === '#' + k.target.id) { a.setAttribute('aria-current', 'true'); }
          else { a.removeAttribute('aria-current'); }
        });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    baglantilar.forEach(function (a) {
      var hedef = document.querySelector(a.getAttribute('href'));
      if (hedef) { gozlem.observe(hedef); }
    });
  }

  /* ---------- 4) "Şimdi açık" göstergesi ---------- */
  var rozet = document.getElementById('acik-rozet');

  function dakika(s) {
    var p = s.split(':');
    return parseInt(p[0], 10) * 60 + parseInt(p[1], 10);
  }

  // Verilen gün ve dakika için açık mı? Gece yarısını aşan vardiyaları da hesaba katar.
  function aciklikBul(gun, dk) {
    var bugun = SAATLER[gun];
    var dun = SAATLER[(gun + 6) % 7];
    if (bugun) {
      var a = dakika(bugun[0]), k = dakika(bugun[1]);
      if (k > a && dk >= a && dk < k) { return true; }
      if (k <= a && dk >= a) { return true; }
    }
    if (dun) {
      var da = dakika(dun[0]), dk2 = dakika(dun[1]);
      if (dk2 <= da && dk < dk2) { return true; }
    }
    return false;
  }

  // Bir sonraki açılış metni (ör. "Salı 09:00")
  function sonrakiAcilis(gun, dk) {
    var adlar = ['Pazar', 'Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'];
    for (var i = 0; i < 8; i++) {
      var g = (gun + i) % 7;
      var s = SAATLER[g];
      if (s && (i > 0 || dakika(s[0]) > dk)) {
        return (i === 0 ? 'bugün ' : adlar[g] + ' ') + s[0];
      }
    }
    return '';
  }

  function rozetiGuncelle() {
    var tanimli = Object.keys(SAATLER).some(function (g) { return SAATLER[g]; });
    if (!rozet || !tanimli) { return; } // saatler girilmediyse gizli kalır
    var simdi = new Date();
    var gun = simdi.getDay();
    var dk = simdi.getHours() * 60 + simdi.getMinutes();
    if (aciklikBul(gun, dk)) {
      rozet.textContent = 'Şu an açığız';
      rozet.classList.remove('kapali');
    } else {
      rozet.textContent = 'Şu an kapalı. Açılış: ' + sonrakiAcilis(gun, dk);
      rozet.classList.add('kapali');
    }
    rozet.hidden = false;
  }

  rozetiGuncelle();
  setInterval(rozetiGuncelle, 60000);
})();
