# YouTube Ajan Ekibi

Bu klasör bir YouTube içerik üretim stüdyosudur. Her zaman **Türkçe** konuş ve yaz.

## Ekip (`.claude/agents/`)
| Ajan | Görev |
|---|---|
| trend-arastirmaci | Trendler, aranan sorular, video fikirleri |
| rakip-analisti | Rakip kanallar, içerik boşlukları |
| nis-stratejisti | Niş, hedef kitle, kanal kimliği, para kazanma |
| senarist | Uzun video senaryosu |
| kanca-uzmani | İlk 5-15 saniye açılışları |
| seo-uzmani | Başlık, açıklama, etiket, bölümler |
| thumbnail-tasarimci | Kapak konsepti + yapay zekâ görsel promptu |
| shorts-uzmani | Shorts/Reels/TikTok senaryoları |
| topluluk-yoneticisi | Yorumlar, topluluk gönderisi, sosyal medya |
| analitik-uzmani | YouTube Studio verisi analizi |
| icerik-planlayici | Haftalık/aylık takvim |
| elestirmen | Yayın öncesi kalite kontrol |

## Çalışma kuralları
- Birbirine bağlı olmayan ajanları **paralel** çalıştır (ör. araştırma + rakip analizi; SEO + thumbnail + Shorts).
- Bir ajanın çıktısı diğerine lazımsa sırayla çalıştır (araştırma → senaryo → paketleme → eleştirmen).
- Tüm çıktılar `cikti/<konu-adi>/` klasörüne numaralı dosyalar olarak kaydedilir.
- Bir video paketi bitince her zaman `elestirmen` ile kontrol et.
- Uydurma istatistik veya kaynaksız iddia kullanma.

## Kısayol komutları
- `/video-paketi <konu>`: tüm ekiple eksiksiz video paketi
- `/kanal-stratejisi <ilgi alanı>`: niş + strateji + 4 haftalık takvim
- `/haftalik-plan <konu, sıklık>`: haftalık fikir ve takvim
- `/shorts <konu>`: 5 Shorts senaryosu
- `/analiz <dosya.csv>`: YouTube Studio verisi analizi
