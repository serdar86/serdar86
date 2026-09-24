# Ürün avı: Ev tekstil / ABD

Bu klasördeki script'ler AIsa üzerinden SECTION 3'ün STEP 0-9 adımlarını sırayla çalıştırır ve `board.html` panosunu üretir.

- `config.json`: SECTION 1 girdileri
- `hunt.py`: bütün adımlar. Ham yanıtlar `raw/` altına yazılır; bir yanıt diskte varsa o çağrı bir daha yapılmaz. Her ücretli adımdan önce bakiye okunur. Bir adım harcama tavanını aşacaksa script durur.
- `PANO.py`: panoyu `measurement.json` dosyasından üretir (prompttaki dosyanın aynısı)

Çalıştırma:

```
AISA_API_KEY=... python3 hunt.py
```

Ortam ağında `api.aisa.one` alan adına izin verilmiş olmalı. Görsellerin panoya gömülebilmesi için `*.aliexpress-media.com`, `ae-pic-*.alicdn.com` ve `i.ytimg.com` alan adlarına da izin verilmeli. Pillow kuruluysa ürün fotoğraflarının renklilik değeri (`renk`) ölçülür. Kurulu değilse `renk` 0 yazılır ve fotoğraflar sıralanmaz.
