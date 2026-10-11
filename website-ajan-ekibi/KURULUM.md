# Kurulum (Windows)

PowerShell aç (Claude Code'un dışında) ve sırayla yapıştır:

```powershell
cd $HOME\Desktop
Invoke-WebRequest https://github.com/serdar86/serdar86/archive/refs/heads/ccr-86dc3c8f-cbqr1p.zip -OutFile ajan.zip
Expand-Archive ajan.zip -DestinationPath ajan-tmp
Copy-Item -Recurse ajan-tmp\serdar86-ccr-86dc3c8f-cbqr1p\website-ajan-ekibi .\web-studyo
Remove-Item -Recurse ajan.zip, ajan-tmp
cd web-studyo
claude
```

Claude Code açılınca `/agents` yaz, 8 ajanı görmelisin. Sonra:

```
/site-yap Kadıköy'de bir kahve dükkânı için tek sayfalık site
```

Bitince `web-studyo\site\index.html` dosyasına çift tıkla, site tarayıcıda açılır.

## ⚠️ Kullanım limiti
`/site-yap` 8 ajan çalıştırır, Pro limitini hızlı harcar. Kalan hakkını `/usage` ile kontrol et.
