# Ringkasan pelantikan pegawai — v002

Status: **DRAF MENUNGGU LUDO**, bukan hasil akhir.

- Brief asal: `source/master-prompt.md`.
- Fakta: teks pengguna daripada projek terdahulu; provenance dan baris rujukan dalam `storyboard.json`.
- Skrip: `outputs/skrip_narasi_bm.md` (616 perkataan).
- Storyboard: `outputs/storyboard_video.md` (8 babak, 29 visual beats).
- Draf visual sebenar: `outputs/DRAF_330s_FHD_TANPA_AUDIO.mp4`, H264, Full HD, 30fps, 330s, tanpa audio. Masa anggaran sahaja.
- Pratonton semua babak: `outputs/Pratonton_8_Babak.png`.
- Fail final, WAV dan SRT akhir **belum dihasilkan**.

Baca `outputs/PANDUAN_LUDO.md` untuk mendapatkan input sebenar. Jangan guna eSpeak atau audio tiruan. Jangan tandakan selesai atau cipta tag terbitan sehingga Ludo, penyegerakan, sari kata, visual dan semakan akhir disahkan.

Dari akar repo, jana semula draf visual dengan `.venv/bin/python videos/ringkasan-tugas-utama-dan-prosedur-pelantikan-pegawai/v002/render_fhd.py --draft`. Semakan fixture setempat: `.venv/bin/python videos/ringkasan-tugas-utama-dan-prosedur-pelantikan-pegawai/v002/verify_pipeline.py`. Fixture hanya menguji logik dan bukan Ludo sebenar.

Selepas WAV Ludo, cues dan rekod semakan sah tersedia, `.venv/bin/python videos/ringkasan-tugas-utama-dan-prosedur-pelantikan-pegawai/v002/finalise.py` akan menjalankan pipeline khusus versi dan mengeksport nama fail diminta. Pipeline akhir dengan Ludo belum diuji; semak laporan QA dan hasil sebelum publish.
