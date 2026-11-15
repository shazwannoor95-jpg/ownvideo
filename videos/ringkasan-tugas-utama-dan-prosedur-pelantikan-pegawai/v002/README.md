# Ringkasan pelantikan pegawai — v002

Status: **Video siap**. Lapan babak, 5 minit 14 saat, Full HD 1080p pada 30 fps. Narasi sintetik menggunakan Ludo dalam Google AI Studio.

- [Video akhir MP4](outputs/Video_Pelantikan_Pegawai_UiTM_Final.mp4) dengan sari kata Bahasa Melayu dan penanda babak.
- [Sari kata SRT](outputs/Video_Pelantikan_Pegawai_UiTM.srt).
- [Skrip narasi](outputs/skrip_narasi_bm.md) dan [storyboard](outputs/storyboard_video.md).
- [WAV Ludo dan cap masa](audio/) untuk setiap babak.
- [Laporan teknikal](qa/final-technical-report.json) dan [rekod semakan narasi](audio/ludo-review.json).

Semakan teknikal mengesahkan nyahkod penuh, format audio dan video serta tempoh garis masa. Semua bahagian skrip disemak melalui transkripsi setempat. Sebutan belum disemak melalui pendengaran manusia.

Jalankan `python finalise.py` dari folder ini untuk menghasilkan semula video menggunakan WAV, cap masa dan storyboard sedia ada. Persekitaran Python memerlukan Pillow, FFmpeg dan FFprobe. Brief asal tersedia dalam `source/master-prompt.md`.
