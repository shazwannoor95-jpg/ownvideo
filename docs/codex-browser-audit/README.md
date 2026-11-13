# Audit Google AI Studio dalam browser Codex

Ujian pada 13 November 2026, waktu Malaysia, menggunakan skrip dan visual babak pembukaan projek pelantikan v002.

| Langkah | Keputusan | Bukti |
| --- | --- | --- |
| Buka editor dan pilih suara | Lulus | Google AI Studio dalam browser Codex memaparkan Gemini 3.8 Flash TTS dan Speaker 1 – Ludo. |
| Jana narasi | Lulus | Butang Run bertukar kepada Stop semasa penjanaan. Pemain kemudian memaparkan audio 14.36 saat. |
| Muat turun manual | Lulus | Pengguna mengklik Download dalam tab AI Studio dan memberikan laluan WAV yang disimpan. Fail itu mengandungi PCM 16 bit, mono, 24 kHz dan berdurasi 14.36 saat. Transkripsi setempat mengesan kedua-dua ayat pembukaan. |
| Muat turun automatik | Belum disahkan | Klik automatik dihantar, tetapi pemerhatian tamat tanpa laluan fail. Kawalan muat turun media menyekat URL `data:` daripada pemain audio. |
| Gabungkan WAV dengan visual | Lulus | FFmpeg menghasilkan MP4 H.264/AAC, 1920 × 1080, 30 fps, 461 bingkai dan 15.37 saat. Nyahkod penuh audio dan video lulus. |

Video ujian meliputi satu babak. Masa visual dilaraskan kepada tempoh audio baharu. Visual ini mengandungi sari kata yang sudah dirender daripada versi asal. Untuk produksi, ukur semula cap masa sari kata daripada setiap WAV baharu. Transkripsi automatik mengesahkan kandungan umum skrip. Sebutan tepat belum disemak melalui pendengaran manusia.

- WAV SHA-256 `3cbd45f101b0f7babee3c501650a8a1b75fb0140c622d27abae383c3f49379d9`
- MP4 SHA-256 `906cdd888d884ef4477d0db02dcdae0e347b630894d1ae1f46bddd5854ac2f52`

[MP4 ujian](Ujian_Browser_Codex_Ludo_v002.mp4) · [WAV ujian](Ujian_Browser_Codex_Ludo_v002.wav)

## Ulang aliran daripada chat atau akaun lain

1. Import atau klon repo dan buka foldernya sebagai projek dalam aplikasi desktop Codex. Ikut bahagian pemasangan dalam [README](../../README.md) untuk menyediakan Python, FFmpeg dan FFprobe pada hos. Mulakan video daripada bahan sumber dengan `./video new "Tajuk" --source <fail-teks>` di Bash, atau `python tools/video.py new "Tajuk" --source <fail-teks>` pada Windows dengan Python yang mempunyai kebergantungan repo.
2. Dalam chat projek, minta Codex sediakan storyboard dan skrip mengikut babak. Buka [Generate Speech](https://aistudio.google.com/generate-speech) dalam browser Codex. Log masuk Google pada profil browser yang digunakan jika diperlukan, pilih **Ludo**, dan jalankan skrip setiap babak. Import repo membawa fail dan arahan projek. Akses browser dan sesi Google bergantung pada akaun serta peranti yang digunakan.
3. Klik **Download** selepas setiap klip siap. Jika Codex belum dapat mengambil fail secara automatik, klik butang itu sendiri dan berikan laluan WAV atau lampirkan fail kepada chat. Codex kemudian boleh memadankan fail mengikut babak, menyimpannya sebagai `audio/sXX.wav`, dan menyediakan `audio/sXX.cues.json` mengikut rakaman sebenar.
4. Jalankan `./video render <folder-projek> --workers 2` di Bash atau `python tools/video.py render <folder-projek> --workers 2` pada Windows. Semak MP4, SRT dan laporan sebelum penerbitan. Untuk mencuba semula video pelantikan v002 dengan aset yang sudah disimpan, ikut [panduan v002](../../videos/ringkasan-tugas-utama-dan-prosedur-pelantikan-pegawai/v002/README.md).

[Lihat tetapan browser Codex](https://learn.chatgpt.com/docs/browser)
