# Keperluan dan pemindahan

| Keperluan | Status |
|---|---|
| `google-ai-studio-voiceover` | Dirujuk oleh `buat-video-motion-grafik/SKILL.md`, baris 20 dan 103. Folder skill berasingan tidak ditemui dalam direktori skills yang diaudit. Pakej ini membina semula dokumentasi berdasarkan rekod. |
| Alat browser automation dan laluan fail | Asal: `mcp__cua_repl.js`, `iab`, akses keadaan UI, Playwright locator pada tab, serta Node untuk menulis fail setempat. Ia datang daripada hos yang menjalankan chat. |
| Google AI Studio | Akaun Google yang pengguna log masuk sendiri, akses kepada Generate Speech, pilihan Ludo jika tersedia, dan kuota mencukupi. Laluan asal melalui UI tidak memerlukan API key. |
| QA dan produksi video | Untuk mengukur WAV: Python `wave` atau FFprobe. Untuk video: Python dan FFmpeg/FFprobe, serta perender projek. ASR Bahasa Melayu membantu audit jika tersedia. Pakej ini tidak membekalkan enjin, model atau fail projek. |
| Skill motion grafik utama | Skill tempatan mengandungi `scripts/add_malay_voiceover.py` serta panduan audio. Rekod eksport WAV melalui CUA menggunakan kod JavaScript dalam panggilan alat. Projek video asal kemudian menjalankan skrip Python miliknya sendiri. |

- **Codex pada PC sama.** Ekstrak folder `google-ai-studio-voiceover`. Lampirkan folder pada chat baharu, atau letakkan di direktori skills Codex yang dipantau oleh pemasangan tersebut dan buka chat baharu. Gunakan `$google-ai-studio-voiceover` jika skill disenaraikan. Sahkan alat pelayar dan akses tab walaupun akaun pernah digunakan pada PC ini.
- **Codex pada komputer lain.** Salin atau ekstrak folder yang sama. Gunakan pelayar dan alat yang tersedia pada komputer itu. Pengguna perlu menyediakan akses Google sendiri. Untuk pemasangan video penuh, sediakan FFmpeg/FFprobe, Python, perender dan aset projek pada mesin sasaran.
- **ChatGPT Work dengan automasi pelayar.** Lampirkan dokumen dan tampal prompt. Pembantu perlu mempunyai akses kepada editor Google AI Studio dan cara menyimpan atau menyerahkan fail. API CUA dan akses Node Windows dalam contoh bergantung pada hos. Jika hanya kawalan visual tersedia, gunakan muat turun biasa atau serahan fail daripada pengguna.

Semakan pakej ini dibuat daripada rekod setempat. Kebolehlaksanaan pada hos baharu bergantung pada alat, antara muka Google, sesi pengguna dan akses fail yang tersedia pada masa penggunaan.