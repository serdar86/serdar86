# Kurulum (Windows)

## 1. İndir ve kur
PowerShell aç (Claude Code'un dışında) ve sırayla yapıştır:

```powershell
cd $HOME\Desktop
Invoke-WebRequest https://github.com/serdar86/serdar86/archive/refs/heads/ccr-86dc3c8f-cbqr1p.zip -OutFile ajan.zip
Expand-Archive ajan.zip -DestinationPath ajan-tmp
Copy-Item -Recurse ajan-tmp\serdar86-ccr-86dc3c8f-cbqr1p\youtube-ajan-ekibi .\youtube-studyo
Remove-Item -Recurse ajan.zip, ajan-tmp
cd youtube-studyo
claude
```

## 2. Kontrol et
Claude Code açılınca yaz:
```
/agents
```
13 ajanı listede görmelisin.

## 3. Kullan
```
/video-paketi evde kahve yapımı
/kanal-stratejisi teknoloji ve yapay zekâ
/haftalik-plan oyun kanalı, 2 uzun 5 shorts
/shorts telefon pil ömrünü uzatma
/analiz C:\Users\samsung\Downloads\youtube-istatistik.csv
```
Ya da normal yaz: "trend-arastirmaci ve rakip-analisti paralel çalışsın, konu: ..."

## ⚠️ Kullanım limiti
`/video-paketi` 9 ajan çalıştırır, Pro limitini hızlı harcar. Kalan hakkını `/usage` ile kontrol et.
Limiti korumak için ajan dosyalarının başındaki `---` bloğuna `model: sonnet` satırı ekleyebilirsin.
