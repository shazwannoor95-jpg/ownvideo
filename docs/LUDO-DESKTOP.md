# ownvideo — Google AI Studio Ludo Desktop

Aplikasi Electron membuka tetingkap Google AI Studio sendiri, menggunakan profil aplikasi berasingan dan login manual pengguna. Selepas skrip disemak serta diluluskan, aplikasi memilih Ludo, mengisi Style dan Speech block text, menekan Run dan menyimpan WAV penuh setiap babak. Tiada API key diperlukan untuk laluan UI ini.

## Pasang

Perlu Node 24+, npm, FFmpeg dalam PATH, dan desktop Windows/macOS/Linux dengan paparan grafik. Electron 45.3.1 dipinkan dalam lockfile. TLS dan semakan checksum installer Electron dikekalkan.

Dari akar repo pada Linux/macOS/Git Bash:

```bash
bash tools/setup-ludo.sh
./ludo
```

Pada Windows PowerShell:

```powershell
npm --prefix desktop ci
node desktop/node_modules/electron/install.js
npm --prefix desktop start
```

Pada hos proksi, gunakan konfigurasi proksi/CA yang dibekalkan; installer Node 24 boleh menggunakan `NODE_USE_ENV_PROXY=1`. Jangan matikan pengesahan TLS. `npm ci` memasang dependency; `install.js` memastikan binary Electron turut dipasang (Electron ini memuat turun binary secara lazy).

## Guna

1. Pilih `storyboard.json` folder versi video, contohnya projek ringkasan `v002`. Jika checkout main tidak mengandungi projek, checkout branch video selepas menyimpan kerja anda; branch v002 lama tidak mempunyai desktop ini. Cara yang sesuai dalam sesi ini ialah membuka aplikasi dari checkout integrasi dan memilih folder projek yang dieksport secara berasingan dengan `git archive`, tanpa checkout/worktree tambahan. Jangan cipta worktree tanpa permintaan pengguna.
2. Semak teks semua babak yang dipaparkan. Buka / login Google AI Studio. Login dan pengesahan akaun mesti dibuat pengguna sendiri dalam tetingkap aplikasi, bukan Chrome lain.
3. Pilih mod satu pembicara pada Generate Speech. Tekan Semak editor. Pengesanan editor tidak mengesahkan pilihan Ludo atau kuota.
4. Tekan Luluskan skrip dan jana WAV Ludo; dialog native mengesahkan jumlah babak/aksara sebelum teks dihantar. Hanya narasi dan gaya dihantar, tanpa PDF/logo/sumber lain.
5. Aplikasi memeriksa label Ludo, medan teks, status Run/Download dan WAV lengkap (menolak perangkap 0.04s). Jika Ludo tiada, kuota gagal atau UI berubah, ia berhenti tanpa menukar suara. Hentikan akan membatalkan kerja adapter; ia tidak menjamin permintaan yang sudah dihantar kepada Google turut dibatalkan.
6. `audio/sXX.wav` disimpan sebagai PCM mono 24kHz. `audio/ludo-generation.json` merekod hash skrip/audio dan durasi sebenar. Ulang kerja menggunakan WAV yang sepadan; WAV asal yang tidak sepadan tidak ditimpa.
7. Dengarkan sebutan dan semak kelengkapan narasi. Status semakan manusia kekal pending. Aplikasi tidak mencipta cues/SRT anggaran sebagai penjajaran sebenar, tidak menandakan `ludo-review.json` lulus, dan tidak merender/publish video secara automatik. Sediakan cues sebenar dan rekod semakan sebelum menjalankan pipeline video.

Tetapan suara dikunci kepada **Ludo**, dengan gaya BM korporat. Google mungkin menolak login melalui embedded browser, atau menukar nama kawalan; jika itu berlaku, jana/import WAV secara manual. Tiada jaminan login atau kuota.

Profil Chromium disimpan secara tempatan dalam `.cache/ludo-profile/`, diabaikan Git. Ia boleh mengandungi cookie login yang diurus Chromium. Kod tidak membaca/mengeksport credential atau menyalin profil ke projek video. Jangan kongsi atau commit profil; logout melalui Google. `OWNVIDEO_LUDO_PROFILE` boleh menunjuk ke direktori peribadi lain di luar repo.

## Cloud dan Desktop Codex

Aplikasi Electron tidak memerlukan token dalaman pelancar browser Codex untuk membuka tetingkap pada desktop biasa. Namun, menjalankannya pada X display maya hanya membolehkan ujian grafik: ia **tidak menyediakan viewer atau kawalan login kepada pengguna Codex**. `./ludo` berhenti dengan arahan jelas jika Linux tiada DISPLAY/Wayland; jangan menganggap aplikasi boleh dilihat pengguna apabila hanya ujian paparan maya dijalankan.

Audit sesi ini menggunakan Xorg dummy berautentikasi dan tanpa TCP, khusus ujian. Audit Google sebenar sampai ke Google Accounts Sign in. Tiada login, pemilihan Ludo di Google sebenar atau penjanaan WAV sebenar diuji. Permintaan latar ke `accounts.youtube.com` pernah gagal polisi proksi; keperluan selepas login belum diketahui. Tiada perubahan tetapan persekitaran atau Publish dilakukan.

## Semakan

```bash
npm --prefix desktop test
npm --prefix desktop run test:electron
npm --prefix desktop run audit:google
```

Dua arahan terakhir memerlukan paparan grafik. Gunakan `OWNVIDEO_LUDO_PROFILE` berasingan untuk audit dan `OWNVIDEO_AUDIT_DIR` untuk lokasi hasil. Audit fixture menggunakan interception HTTPS setempat dan tidak menghubungi Google. Audit langsung hanya membuka/menyemak halaman dan menyimpan screenshot; ia tidak login atau menekan Run. Jangan kongsi screenshot jika anda menjalankannya dengan profil yang mengandungi maklumat akaun. Laporan yang dibundel ada di `docs/ludo-audit/`.

Keputusan sesi ini: **11 ujian unit lulus**, **7 pemeriksaan Electron fixture lulus**. Audit langsung merekod `LOGIN_REQUIRED`; pemilihan Ludo dan WAV sebenar masih **NOT_RUN**. Senarai host permintaan latar yang gagal berada dalam JSON audit; ia tidak membuktikan semuanya perlu dibenarkan atau mempunyai punca kegagalan sama. Windows/macOS belum diuji. Tiada dakwaan STABLE atau video siap dibuat.
