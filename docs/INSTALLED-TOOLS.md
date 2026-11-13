# Skill, preset dan keupayaan produksi

Skill repo dipasang di `.agents/skills/` dan tersedia untuk hos Codex yang menemui skill repo. Mulakan sesi baharu untuk penemuan semula jika perlu, atau baca SKILL.md secara terus. Tiada salinan global diperlukan.

| Komponen | Lokasi / status |
|---|---|
| Google AI Studio voiceover | `.agents/skills/google-ai-studio-voiceover/`: semua enam dokumen lampiran dipadankan byte demi byte; nama fail dinormalkan untuk pautan Linux |
| Motion grafik BM | `.agents/skills/buat-video-motion-grafik/`: skill pembungkus, prompt asal tanpa perubahan dan manifest SHA256 |
| Preset Ludo | `presets/motion-grafik-bm-ludo.json`: brief Full HD, 30fps, putih, Ludo, H264/AAC dan sari kata; bukan konfigurasi automatik renderer |
| Python dan dependency | `bash tools/setup.sh`, `.venv`, dependency dipinkan dalam `requirements-lock.txt` |
| FFmpeg/FFprobe | Disediakan mesin; libx264 dan AAC tersedia |
| Chromium + Playwright | Tersedia pada hos semasa; pembukaan halaman setempat dan locator butang telah lulus. Bukan extension CUA asal dan bukan bukti akses Google |
| CUA / iab / extension | Tiada pakej extension, URL pemasangan atau kod alat hos dibekalkan. Tidak boleh dipasang daripada rujukan dokumentasi sahaja |
| Google AI Studio / Ludo | Memerlukan akses rangkaian, akaun, pilihan Ludo dan kuota. Permintaan HTTPS semasa ditolak proksi dengan 403; belum diuji dalam editor atau menghasilkan WAV |
| ASR / skrip motion grafik lama | Model ASR dan `scripts/add_malay_voiceover.py` tidak dilampirkan; bukan sebahagian pemasangan ini |

Semua narasi produksi pengguna mesti Google AI Studio Ludo. `render` tidak lagi menjana eSpeak secara automatik. WAV dan cues yang tiada menghentikan render; `--resynthesize` memberi arahan untuk menjana semula Ludo. WAV sedia ada tidak membuktikan penyedia atau suara; semak dalam UI dan simpan bukti produksi. Modul eSpeak lama dikekalkan untuk sejarah, bukan laluan produksi.

Renderer semasa masih 1280×720 dengan kapsyen pilihan. Brief 1920×1080 dan kapsyen dipaparkan memerlukan penyesuaian pipeline sebelum sesuatu hasil boleh didakwa memenuhi brief tersebut. Tiada video baharu dijana oleh pemasangan ini.

Semakan: `PIP_NO_CACHE_DIR=1 bash tools/setup.sh` dan `.venv/bin/python -m unittest discover -s tests -v`. Ujian lifecycle menggunakan nada ujian tanpa pertuturan, remote Git setempat dan render sebenar. Ujian itu tidak menjana Ludo atau mengesahkan sebutan. Dua ujian polisi memastikan audio yang tiada dan `--resynthesize` tidak memulakan pipeline/fallback.

Untuk akses Google dalam cloud ini, semak draf tetapan rangkaian: `aistudio.google.com`, `accounts.google.com`, `www.gstatic.com`, `ssl.gstatic.com`. Dua domain terakhir ialah aset UI dan domain akaun ialah login; keperluan tambahan perlu dikenal pasti daripada UI semasa. Simpan tetapan dan Publish persekitaran untuk tugasan seterusnya. Login pengguna, kuota dan pilihan suara tetap perlu disahkan selepas akses tersedia. Jangan simpan cookie atau credential dalam Git.
