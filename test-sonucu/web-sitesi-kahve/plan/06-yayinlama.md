# Yayınlama Rehberi: Siteyi İnternete Koyma

Bu rehber Windows kullanan, teknik bilgisi az biri için yazıldı. Komut yazmanız gerekmez. Her şey tarayıcıdan ve fare ile yapılır.

> Bu rehber sadece anlatır. Hesapları ve yayını **siz** yapacaksınız. Şifrelerinizi kimseyle paylaşmayın.

---

## 0. Yayından önce: 5 dakikalık kontrol

Sitenizin klasörü: `site` (içinde `index.html`, `css`, `js`, `img` var).

Yayından önce şunları yapın:

1. `site\index.html` dosyasına çift tıklayın. Site tarayıcıda açılıyor mu? Açılıyorsa klasör sağlam demektir.
2. Sitede hâlâ `[DOLDUR: ...]` yazan yerler var. Bunlar telefon, adres, saatler, fiyatlar gibi gerçek bilgilerdir. **Yayından önce hepsini doldurun.** Doldurmadan yayınlarsanız müşteriler "[DOLDUR: telefon]" yazısını görür.
   - Kolay kontrol: `index.html` dosyasını Not Defteri ile açın, `Ctrl + F` ile `DOLDUR` arayın. Hiç sonuç kalmayana kadar düzeltin. (Bunu yapmak için `gelistirici` ajanından yardım isteyebilirsiniz.)
3. `#DOLDUR-harita-linki`, `#DOLDUR-telefon`, `#DOLDUR-instagram` gibi bağlantılar da gerçek adresle değişmeli. Yoksa düğmeler çalışmaz.
4. Önemli: `site` klasörünün **içinde** `index.html` doğrudan görünmelidir. (Klasörün içinde bir klasör daha varsa, yükleme yaparken yanlış klasörü sürüklemiş olursunuz.)

Not: Sitede şu an **iletişim formu yok**. İletişim; telefon, Instagram ve yol tarifi düğmeleriyle yapılıyor. Form istiyorsanız 4. bölüme bakın. Ayrıca `sitemap.xml` ve `robots.txt` dosyaları henüz `site` klasöründe yok. Bunları `seo-uzmani` ajanı hazırlayacak. 5. bölümdeki sitemap adımı o dosya hazır olunca yapılır.

---

## 1. En kolay yol (önerilen): Netlify Drop

Netlify Drop ile `site` klasörünü tarayıcıya sürükleyip bırakırsınız. Birkaç dakikada site yayında olur.

### Adım adım

1. Tarayıcıda **https://app.netlify.com/drop** adresini açın. (Açılmazsa Google'da "Netlify Drop" yazıp resmi sayfaya girin.)
2. Bilgisayarınızda **Dosya Gezgini**'ni açın. `site` klasörünün bulunduğu yere gidin.
3. `site` klasörünü **fare ile tutup** tarayıcıdaki "Drop your folder here" (klasörünüzü buraya bırakın) kutusuna **sürükleyin ve bırakın**.
   - Sürüklediğiniz şey `site` klasörünün kendisi olsun. İçindeki tek tek dosyaları değil.
4. Birkaç saniye bekleyin. Yükleme bitince size şuna benzer bir adres verir: `rastgele-isim-12345.netlify.app`.
5. Bu adrese tıklayın. Siteniz açılıyorsa yayındasınız.
6. **Hesap açın (önemli).** Hesap açmadan yüklenen site kısa süre sonra silinebilir. Sayfada "Claim" / "Sign up" (sahiplen / kayıt ol) benzeri bir düğme çıkar. Ona basıp e-posta veya Google hesabınızla kayıt olun. Tam süreyi ve düğme adını ekranda kontrol edin; Netlify arayüzü zamanla değişebilir.
7. Site adını değiştirin (isteğe bağlı):
   - Netlify panelinde sitenize girin.
   - **Site configuration** (Site ayarları) bölümünü açın.
   - **Change site name** (Site adını değiştir) düğmesine basın.
   - Örnek: `kadikoy-kahve-evi` yazın. Yeni adres `kadikoy-kahve-evi.netlify.app` olur. Boşluk ve Türkçe harf (ç, ş, ğ, ı, ö, ü) kullanmayın.

### Siteyi güncellemek (fiyat değişti, saat değişti)

1. Dosyayı düzeltin (örneğin `index.html`) ve kaydedin.
2. Netlify panelinde sitenize girin, **Deploys** (Yayınlar) sekmesini açın.
3. Sayfanın altında "Drag and drop your site output folder here" benzeri bir alan vardır. Güncel `site` klasörünü oraya yine sürükleyip bırakın.
4. Eski adres aynı kalır, içerik yenilenir.

### Artıları ve eksileri

| Artı | Eksi |
|---|---|
| Komut yok, sadece sürükle-bırak | Her değişiklikte klasörü elle yeniden yüklersiniz |
| HTTPS (kilit işareti) otomatik | Ücretsiz planın aylık kullanım sınırı var (aşağıya bakın) |
| Form özelliği hazır (Netlify Forms) | Limit dolarsa site duraklayabilir (kaynaklara göre) |
| Kendi alan adınızı kolay bağlarsınız | Arayüz zamanla değişebilir |

---

## 2. Alternatifler

### 2.1 Cloudflare Pages (sürükle-bırak ile)

Küçük bir dükkân sitesi için sağlam ve hızlı bir seçenektir. Ücretsiz planı cömerttir.

1. **https://dash.cloudflare.com** adresinden ücretsiz hesap açın.
2. Sol menüde **Workers & Pages** bölümüne girin.
3. **Create application** (Uygulama oluştur) düğmesine basın.
4. **Pages** sekmesini seçin, sonra **Upload your static files** / **Drag and drop your files** (dosyalarını sürükle-bırak) seçeneğini seçin.
5. Proje adı yazın (örnek: `kadikoy-kahve-evi`). Küçük harf ve tire kullanın.
6. `site` klasörünü kutuya sürükleyin. (Klasör sürüklemek olmazsa `site` klasörünü zip yapıp yükleyebilirsiniz; Cloudflare zip veya klasörü kabul eder.)
7. **Deploy** düğmesine basın. Adres: `proje-adi.pages.dev`.

Menü adları değişmiş olabilir. Ekranda "Pages" ve "Upload" benzeri kelimeleri arayın. Cloudflare'in kendi anlatımı: [Direct Upload belgesi](https://developers.cloudflare.com/pages/platform/direct-upload/).

| Artı | Eksi |
|---|---|
| Ücretsiz plan cömert; Cloudflare belgesine göre ücretsizde dosya sayısı ve boyut sınırları küçük site için fazlasıyla yeterli ([sınırlar](https://developers.cloudflare.com/pages/platform/limits)) | Menüler Netlify'a göre biraz daha teknik görünür |
| Hızlı, dünya çapında dağıtım | Form özelliği yok; form için Formspree gibi ayrı servis gerekir |
| Alan adını Cloudflare'den de alabilirsiniz (.com) | Cloudflare .com.tr satmaz (kontrol edin) |

### 2.2 GitHub Pages

Komut gerektirmez ama biraz daha fazla adım vardır. Dosyalar GitHub sitesine tarayıcıdan yüklenir.

1. **https://github.com** adresinden ücretsiz hesap açın.
2. Sağ üstteki **+** işaretine, sonra **New repository** (yeni depo) seçeneğine basın.
3. Ad yazın (örnek: `kafe-sitem`). **Public** (herkese açık) seçin. **Create repository** deyin.
4. Açılan sayfada **uploading an existing file** bağlantısına tıklayın.
5. `site` klasörünün **içindekileri** (`index.html`, `css`, `js`, `img`) seçip sürükleyin. Klasörlerin de yüklendiğinden emin olun. **Commit changes** düğmesine basın.
6. **Settings** (Ayarlar) > **Pages** bölümüne girin.
7. "Build and deployment" altında **Source: Deploy from a branch** seçin. Branch olarak **main** ve klasör olarak **/ (root)** seçin. **Save** deyin.
8. 1-3 dakika bekleyin. Adres: `kullaniciadi.github.io/kafe-sitem`.

| Artı | Eksi |
|---|---|
| Ücretsiz, uzun yıllardır var | Depo herkese açık olur (içindeki her şey görünür) |
| Dosya geçmişi tutulur | Adım sayısı daha fazla; yeni başlayan için karışık |
| | Form özelliği yok |
| | Adres alt klasörlü olabilir (`/kafe-sitem`); sitedeki yollar göreli olduğu için çalışması beklenir, yine de açıp kontrol edin |

### 2.3 Hangisini seçmeli?

| Durum | Öneri |
|---|---|
| "Hızlıca yayınlayayım, form da isterim" | **Netlify Drop** |
| "Ücretsiz sınırlar çok rahat olsun" | Cloudflare Pages |
| "GitHub'ı zaten kullanıyorum" | GitHub Pages |

---

## 3. Alan adı (www.kafeadiniz.com)

Netlify/Cloudflare size ücretsiz bir adres verir (`...netlify.app`). Müşteriye `kafeadiniz.com` gibi kendi adresiniz daha güven verir. Google'da bulunmak için de iyidir. Alan adı **ücretlidir** ve **yıllık** ödenir.

### 3.1 Ad seçimi

- Kısa, kolay yazılan, Türkçe harfsiz olsun. Örnek: `kadikoykahve.com`
- ç, ş, ğ, ı, ö, ü kullanmayın (`kadikoy` yazın, `kadıköy` değil).
- Tire ve rakamdan kaçının.
- Telefonda söylerken karışmasın.

### 3.2 .com mu, .com.tr mi?

| | .com | .com.tr |
|---|---|---|
| Kimler için | Herkes | Türkiye odaklı siteler |
| Nereden alınır | Namecheap, GoDaddy, Cloudflare, Türk firmaları (Turhost, Natro vb.) | Türkiye'deki yetkili kayıt kuruluşları (TRABİS sistemi) |
| Fiyat | Genelde yıllık yaklaşık 10-15 dolar civarı (kontrol edin) | Firmaya göre değişir; firmaların fiyat listesine bakın |
| Not | Her yerde tanınır | Belge isteyip istemediğini alırken kontrol edin |

**.com.tr için not:** Bir ticaret blogu, 2020 sonrası TRABİS düzeninde .com.tr için belge istenmediğini yazıyor ([kaynak](https://birfatura.com/domain-nasil-alinir-alan-adi-tescil/)). Bu bilgi resmî değil. Satın almadan önce seçtiğiniz firmanın sayfasında şartları **kontrol edin**. Resmî bilgi için BTK / TRABİS sitelerine bakın.

**Öneri:** Önce `.com` bakın. Müsait değilse `.com.tr` deneyin. İkisi de alınırsa asıl adres olarak `.com` kullanın, diğerini yönlendirin (ya da boş bırakın).

### 3.3 Nasıl alınır (genel adımlar)

1. Alan adı satan bir firmanın sitesine girin (Türkiye'de Turhost, Natro, İsimtescil gibi firmalar var; hepsinin fiyatını karşılaştırın).
2. Arama kutusuna istediğiniz adı yazın (örnek: `kadikoykahve`).
3. Müsait olan uzantıyı sepete ekleyin.
4. **Gereksiz ek hizmetleri sepetten çıkarın** (hosting, e-posta paketi, SSL paketi, "gizlilik koruması" ücretleri çoğu zaman gerekmez). Siteniz Netlify veya Cloudflare'de yayınlanacağı için ayrıca hosting almanıza gerek yok. SSL (HTTPS) de ücretsiz gelecek.
5. Kendi adınıza, doğru bilgilerle kaydolun. Alan adı **sizin adınıza** kayıtlı olmalı (başkasının adına değil).
6. Ödemeyi yapın. Alan adı çoğu zaman birkaç dakikada aktif olur.
7. Satın aldığınız firmanın panelinde **DNS ayarları** (DNS Yönetimi) bölümünü bulun. Aşağıdaki adım için lazım olacak.

### 3.4 Alan adını siteye bağlama (DNS)

DNS, alan adının "hangi siteye gideceğini" söyleyen adres defteridir. Netlify için en kolay yol:

**Yol A: Netlify'a nameserver (ad sunucusu) vermek (önerilen)**

1. Netlify panelinde sitenize girin.
2. **Domain management** (Alan adı yönetimi) bölümünü açın.
3. **Add a domain** / **Add custom domain** (özel alan adı ekle) düğmesine basın.
4. Alan adınızı yazın (örnek: `kadikoykahve.com`). Onaylayın.
5. Netlify "Set up Netlify DNS" benzeri bir seçenek sunar. Onu seçin. Size **4 tane nameserver** adresi gösterir (`dns1.p01.nsone.net` gibi görünür; sizinkini panelden okuyun, burada yazanı kopyalamayın).
6. Alan adını aldığınız firmanın paneline girin. **Nameserver** / **Ad sunucuları** / **DNS sunucuları** ayarını bulun.
7. Varsayılan sunucuların yerine Netlify'ın verdiği 4 adresi yazın. Kaydedin.

**Yol B: Nameserver'ı değiştirmeden kayıt eklemek**

Alan adı firmanızın DNS panelinde Netlify'ın istediği kayıtları (ana alan için A kaydı, `www` için CNAME kaydı) elle eklersiniz. Hangi değerleri yazacağınızı **Netlify'ın domain sayfası size gösterir**; sizin sitenize özel verdiği değerleri yazın. Bu yol biraz daha teknik; takılırsanız Yol A'yı deneyin.

**Cloudflare Pages'te:** Projenize girin, **Custom domains** (özel alan adları) sekmesi > **Set up a custom domain**. Ekrandaki yönergeleri izleyin. Alan adı Cloudflare'de değilse nameserver'ı Cloudflare'e çevirmeniz istenebilir.

**GitHub Pages'te:** Settings > Pages > **Custom domain** kutusuna alan adını yazın ve Save deyin. DNS kayıtlarını GitHub'ın yardım sayfasına göre yapın.

### 3.5 Bekleme süresi ve HTTPS

- DNS değişikliğinin yayılması **birkaç dakikadan 24 saate** kadar sürebilir (bazen 48 saat). Sabırlı olun. Bu sürede site bazen açılır bazen açılmaz; normaldir.
- **HTTPS (adres çubuğundaki kilit) otomatik gelir.** Netlify, Cloudflare Pages ve GitHub Pages ücretsiz sertifika verir. Siz bir şey yapmazsınız. Netlify'da **Domain management > HTTPS** bölümünde sertifikanın hazır olduğunu görebilirsiniz. Birkaç dakika sürebilir; gelmezse "Verify DNS configuration" ve "Provision certificate" benzeri düğmelere basın.
- Kontrol: Tarayıcıda `https://kadikoykahve.com` yazın. Kilit işareti varsa tamam.
- `www.` ile ve `www.` olmadan her iki adres de aynı siteye gitmeli. Netlify bunu genelde kendi ayarlar; bir tanesini "ana adres" seçin.

### 3.6 Alan adından sonra sitede değişecekler

Alan adı belli olunca `index.html` içinde şu satırlar açılıp doldurulmalı (yorum içindeki `<!-- ... -->` işaretlerini kaldırın):

- `og:image` ve `og:url` satırları: `https://[DOLDUR: alan adı]/...` yerine gerçek adres.
- `sitemap.xml`, `robots.txt` ve (varsa) JSON-LD içindeki adresler.

Bunu `gelistirici` veya `seo-uzmani` ajanına yaptırın, sonra klasörü Netlify'a yeniden sürükleyin.

---

## 4. İletişim formu (isteğe bağlı)

**Mevcut durum:** `index.html` içinde `<form>` yok. Müşteri sizi telefonla arıyor, Instagram'a gidiyor ya da yol tarifi alıyor. Brief'te de ana hedef "yol tarifi al". Bir kafe için çoğu zaman form **gerekmez**. İsterseniz şu yolu izleyin:

### Seçenek A: Netlify Forms (Netlify'da yayınlıyorsanız en kolayı)

Form eklenecek yer: `index.html` içinde `id="iletisim"` bölümü. Forma şu hâli verilir (bu kodu `gelistirici` ajanı ekler):

```html
<form name="iletisim" method="POST" data-netlify="true" netlify-honeypot="bot-alani">
  <p hidden><label>Boş bırakın: <input name="bot-alani"></label></p>
  <label for="ad">Adınız</label>
  <input id="ad" name="ad" type="text" required>
  <label for="eposta">E-posta</label>
  <input id="eposta" name="eposta" type="email" required>
  <label for="mesaj">Mesajınız</label>
  <textarea id="mesaj" name="mesaj" required></textarea>
  <button class="dugme" type="submit">Gönder</button>
</form>
```

**Koddaki önemli satır:** `<form name="iletisim" method="POST" data-netlify="true" ...>`. `data-netlify="true"` Netlify'a "bu formu yakala" der. Bu olmadan form çalışmaz.

Kurulum adımları:

1. Formu ekleyin, `site` klasörünü Netlify'a **yeniden yükleyin** (Netlify formu yükleme sırasında bulur).
2. Netlify panelinde **Forms** sekmesine bakın. "iletisim" formu listede görünmeli.
3. Mesajlar e-postanıza gelsin: **Site configuration > Forms > Form notifications > Add notification > Email notification**. E-postanızı yazın. (Menü adlarını ekranda kontrol edin.)
4. Kendiniz bir deneme mesajı gönderin.

Netlify'ın form limiti krediye bağlıdır: resmî değişiklik duyurusuna göre her form gönderimi 1 kredi harcar, spam olarak yakalananlar ücretsizdir ([Netlify duyurusu](https://www.netlify.com/changelog/netlify-pricing-update-introducing-credit-based-plans/)). Bir kafe için bu limit yeterli olmalı; güncel hâlini **kontrol edin**.

### Seçenek B: Formspree (Cloudflare veya GitHub Pages'te yayınlıyorsanız)

1. **https://formspree.io** adresinden ücretsiz hesap açın.
2. **New form** (yeni form) oluşturun, e-postanızı yazın.
3. Formspree size şuna benzer bir adres verir: `https://formspree.io/f/xxxxxxxx` (`xxxxxxxx` sizin formunuzun kodudur).
4. Formu şöyle yazın:

```html
<form action="https://formspree.io/f/xxxxxxxx" method="POST">
  <label for="ad">Adınız</label>
  <input id="ad" name="ad" type="text" required>
  <label for="eposta">E-posta</label>
  <input id="eposta" name="email" type="email" required>
  <label for="mesaj">Mesajınız</label>
  <textarea id="mesaj" name="mesaj" required></textarea>
  <button class="dugme" type="submit">Gönder</button>
</form>
```

**Koddaki önemli satır:** `<form action="https://formspree.io/f/xxxxxxxx" ...>`. `xxxxxxxx` yerine Formspree panelindeki **kendi kodunuzu** yazın.

Formspree ücretsiz planı kaynaklarda genelde ayda 50 gönderim olarak geçiyor, ama kaynaklar çelişiyor. **https://formspree.io/plans** sayfasından güncel limiti kontrol edin ([özet kaynak](https://agentdeals.dev/vendor/formspree)).

### Hangisi?

| | Netlify Forms | Formspree |
|---|---|---|
| Nerede çalışır | Sadece Netlify | Her yerde |
| Kurulum | Tek özellik (`data-netlify`) | Hesap + kod adresi |
| Spam koruması | Hazır (honeypot, otomatik) | Hazır |

Forma teşekkür mesajı için ayrı bir sayfa (`tesekkurler.html`) gerekebilir; bunu istediğinizde `/sayfa-ekle` ile ekletin.

---

## 5. Yayın sonrası: Google'da görünmek

Site yayında ve alan adı bağlıyken yapın. Bunlar ücretsizdir.

### 5.1 Google Search Console (siteyi Google'a tanıtma)

1. **https://search.google.com/search-console** adresine gidin. Google hesabınızla girin.
2. **Add property** (Mülk ekle) deyin. İki seçenek çıkar:
   - **URL prefix** (URL öneki): `https://kadikoykahve.com/` yazın. **Yeni başlayanlar için bu daha kolay.**
   - **Domain**: DNS'te kayıt eklemeyi gerektirir.
3. Sahipliği doğrulayın. URL prefix için en kolay yollar:
   - **HTML file:** Google bir dosya verir (`googleXXXX.html`). Dosyayı `site` klasörüne koyun, klasörü Netlify'a yeniden yükleyin, sonra Search Console'da **Verify** deyin.
   - veya **HTML tag:** Google bir `<meta>` satırı verir. Bunu `index.html` içinde `<head>` bölümüne ekletin, yeniden yükleyin, **Verify** deyin.
4. Doğrulandıktan sonra sol menüden **Sitemaps** bölümüne girin.
5. Kutuya `sitemap.xml` yazın, **Submit** (Gönder) deyin. (Bu dosya `site` klasöründe olmalı. Şu an yok; `seo-uzmani` hazırlayınca ekleyin ve yayını güncelleyin. Önce `https://kadikoykahve.com/sitemap.xml` adresini tarayıcıda açıp göründüğünü kontrol edin.)
6. Sol üstteki arama kutusuna ana sayfa adresinizi yazın ve **Request indexing** (Dizine eklenmesini iste) deyin.
7. Google sitenizi bulmak için günler hatta haftalar alabilir. Sabırlı olun.

Not: Yeni siteler hemen çıkmaz. "Site:kadikoykahve.com" diye Google'da aratarak sitenin indekslenip indekslenmediğine bakabilirsiniz.

### 5.2 Google İşletme Profili (haritada ve "yakınımdaki kafe" aramasında çıkmak)

Bir kafe için **en önemli** adım budur. Müşteriler çoğunlukla Google Haritalar'dan bulur.

1. **https://www.google.com/business** adresine gidin. **Şimdi başla / Get started** deyin.
2. Google hesabınızla girin.
3. İşletme adını yazın. **Gerçek adınızı** yazın (içine "Kadıköy en iyi kahve" gibi kelimeler eklemeyin; Google bunu yasaklar).
4. Kategori: **Kafe** / **Kahve dükkânı** (ekrandaki listeden seçin).
5. Fiziksel adresiniz var mı sorusuna **Evet** deyin, adresi eksiksiz yazın. Haritada konumu iğneyle doğrulayın.
6. Telefon ve **web sitesi** alanına alan adınızı yazın (`https://kadikoykahve.com`).
7. **Doğrulama:** Google adresinizin gerçek olduğunu kanıtlamanızı ister. Posta kartı, telefon, e-posta ya da video seçeneği çıkabilir; yöntem işletmeye göre değişir. Ekrandaki yönergeyi izleyin.
8. Doğrulanınca doldurun:
   - Çalışma saatleri (sitedeki saatlerle **aynı** olsun)
   - Fotoğraflar (dükkân içi, kahve, dış cephe)
   - Menü ve ürünler
   - Olanaklar (Wi-Fi, açık alan gibi, **gerçek** olanlar)
9. Müşterilerden **gerçek yorum** isteyin. Profilinizin bağlantısını QR kod yapıp kasaya koyabilirsiniz. Sahte yorum yazmayın veya satın almayın.
10. Profildeki "Yol tarifi" bağlantısını kopyalayıp `index.html` içindeki `#DOLDUR-harita-linki` yerine yazdırın. Harita gömme kodunu da (`Paylaş > Harita yerleştir`) aynı şekilde sitede açtırın.

**Önemli tutarlılık kuralı:** Adres, telefon ve saatler sitede, Google profilinde ve Instagram'da **birebir aynı** olmalı. Farklı yazılırsa Google'ın güveni azalır.

---

## 6. Maliyet tablosu

Fiyatlar **yaklaşık**tır ve zamanla değişir. Satın almadan önce ilgili sayfadan **kontrol edin**. Kur farkı nedeniyle Türk lirası karşılığı da değişir.

| Kalem | Ücretsiz mi? | Yaklaşık maliyet | Kaynak / not |
|---|---|---|---|
| Netlify (Drop ile yayın, ücretsiz plan) | Evet | 0 | Ücretsiz plan kredi limitli (300 kredi); üretim yayını 15, form gönderimi 1 kredi sayılıyor. Limit dolarsa projeler duraklayabilir. [Netlify duyurusu](https://www.netlify.com/changelog/netlify-pricing-update-introducing-credit-based-plans/), [fiyat sayfası](https://www.netlify.com/pricing). Kontrol et |
| Cloudflare Pages (ücretsiz) | Evet | 0 | Ayda 500 yayın (build), sitede 20.000 dosya, tek dosya 25 MiB sınırı. [Cloudflare sınırlar](https://developers.cloudflare.com/pages/platform/limits). Kontrol et |
| GitHub Pages | Evet | 0 | Ücretsiz hesapta depo herkese açık olur. [GitHub Pages belgesi](https://docs.github.com/pages). Kontrol et |
| HTTPS / SSL sertifikası | Evet | 0 | Üç platformda da otomatik |
| Netlify Forms | Ücretsiz kredi içinde | 0 (limit içinde) | Limit aşılırsa ücretli. Kontrol et |
| Formspree | Evet, sınırlı | 0 (ücretsiz planda) | Kaynaklarda ayda 50 gönderim yazıyor, çelişki var. [formspree.io/plans](https://formspree.io/plans) sayfasından kontrol et |
| .com alan adı | Hayır | Yıllık yaklaşık 10-15 dolar | Cloudflare için üçüncü taraf takipçiler yıllık yaklaşık 10,46 dolar gösteriyor (resmî sayfadan doğrulanmadı). [Örnek takipçi](https://www.whtop.com/plans/cloudflare.com/135912). Firmalara göre değişir, yenileme fiyatına dikkat. Kontrol et |
| .com.tr alan adı | Hayır | Firmaya göre değişir; fiyat bulunamadı | Birkaç yetkili firmanın fiyatını karşılaştırın. Kontrol et |
| Google Search Console | Evet | 0 | |
| Google İşletme Profili | Evet | 0 | |
| Kurumsal e-posta (`info@kadikoykahve.com`) | Genelde hayır | Firmaya göre değişir | İsteğe bağlı. Gmail adresi de kullanılabilir |
| Hosting satın almak | Gerekmez | - | Bu site statik; ücretsiz platformlar yeter |

### Gerçekçi toplam

- **Sadece yayın (adres: `...netlify.app`):** 0 TL.
- **Kendi alan adıyla:** yılda sadece alan adı ücreti. Gerisi ücretsiz.

---

## 7. Hepsi bir arada kontrol listesi

- [ ] `[DOLDUR: ...]` yazılarının hepsi gerçek bilgiyle değişti
- [ ] Telefon, Instagram, yol tarifi bağlantıları çalışıyor
- [ ] Siteyi yerelde açıp telefonda da kontrol ettim
- [ ] `site` klasörünü Netlify Drop'a sürükleyip bıraktım, adres açılıyor
- [ ] Netlify hesabı açtım ve siteyi sahiplendim
- [ ] (İsteğe bağlı) Alan adı aldım, DNS ayarladım, kilit işareti geldi
- [ ] `og:url`, `og:image`, sitemap ve robots adresleri gerçek alan adıyla güncellendi
- [ ] (İsteğe bağlı) İletişim formu eklendi ve deneme mesajı geldi
- [ ] Google Search Console'a ekledim, sitemap gönderdim
- [ ] Google İşletme Profili açtım ve doğruladım
- [ ] Adres, telefon ve saatler her yerde aynı

## 8. Takılırsanız

- Site açılmıyor: Birkaç dakika bekleyin; tarayıcıda `Ctrl + F5` ile yenileyin.
- Düğmeler çalışmıyor: `#DOLDUR-...` bağlantıları değişmemiş olabilir.
- Resimler veya stil görünmüyor: `site` klasörünün **kendisini** değil üst klasörü sürüklemiş olabilirsiniz; `index.html` ilk seviyede görünmeli.
- Alan adı açılmıyor: DNS yayılması 24 saate kadar sürebilir.
- Her şey yolunda ama emin değilseniz: `/site-kontrol` komutuyla kalite ve SEO kontrolü yaptırın.
