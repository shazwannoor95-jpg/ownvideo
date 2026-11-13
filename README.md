# ownvideo

Alat dan arkib produksi video Bahasa Melayu. Setiap video mempunyai branch dan versi sendiri yang dijana daripada tajuk.

Video pertama: [Enam Jenis Pelantikan Pegawai — BARU UiTM](https://github.com/shazwannoor95-jpg/ownvideo/tree/video/enam-jenis-pelantikan-pegawai-baru-uitm/v001).

**[Muat turun MP4 — 13 minit 55 saat, 47 babak (36.8 MB)](https://github.com/shazwannoor95-jpg/ownvideo/raw/68aed8891e2b3d0ad330f4dd7b90d8b3e210a09b/videos/enam-jenis-pelantikan-pegawai-baru-uitm/v001/outputs/enam-jenis-pelantikan-pegawai-baru-uitm-v001-kapsyen.mp4?download=1)**

Video v002: [Ringkasan Tugas Utama dan Prosedur Pelantikan Pegawai](videos/ringkasan-tugas-utama-dan-prosedur-pelantikan-pegawai/v002) · 5 minit 14 saat · 8 babak · Full HD · narasi Ludo.

**[Muat turun MP4 v002](https://github.com/shazwannoor95-jpg/ownvideo/raw/4f242a77c2d3e05a74d12bd7bd494e96d24e9e65/videos/ringkasan-tugas-utama-dan-prosedur-pelantikan-pegawai/v002/outputs/Video_Pelantikan_Pegawai_UiTM_Final.mp4?download=1)** · [Sari kata Bahasa Melayu](videos/ringkasan-tugas-utama-dan-prosedur-pelantikan-pegawai/v002/outputs/Video_Pelantikan_Pegawai_UiTM.srt)

Arahan berterusan untuk agent: muat naik setiap video yang siap bersama fail kerja dan alat yang diperlukan, kemudian berikan pautan muat turun GitHub. Branch serta tag versi dijana mengikut tajuk melalui workflow di bawah. Arahan operasi disimpan dalam `AGENTS.md`.

## Mula dari chat atau agent baru

Buka repo ini pada `main`, lampirkan bahan dan beri brief. Gunakan prompt berikut jika agent memerlukan titik mula.

> Baca AGENTS.md. Gunakan bahan dan brief yang saya lampirkan untuk siapkan video MP4 Bahasa Melayu. Jana narasi Ludo untuk setiap babak, selaraskan sari kata, semak video akhir dan berikan pautan muat turun.

[AGENTS.md](AGENTS.md) menyimpan aliran penuh daripada sumber hingga publish. [Audit browser Codex](docs/codex-browser-audit/README.md) mendokumenkan pilihan UI dan ujian muat turun WAV manual.

## Pasang

Python 3.12+, FFmpeg/FFprobe dengan libx264 dan AAC, serta Git diperlukan. Pada Ubuntu/Debian, pasang pakej sistem melalui pengurus pakej yang dibenarkan oleh mesin anda. Tiada GPU diperlukan. Untuk narasi, ikut setup Gemini API atau UI Google AI Studio di bawah.

```bash
bash tools/setup.sh
```

Pemasangan menggunakan `.venv` berasingan. Fon, ikon, logo, lesen, renderer, penjana muzik dan alat semakan dibundel dalam `tools/template/`. Ia tidak bergantung pada repo lain atau fail dalam komputer asal.

## Jana narasi Ludo

Simpan `GEMINI_API_KEY` dalam secret persekitaran yang menjalankan skrip. GitHub Codespaces memuatkan Codespaces secret untuk repo ini. Untuk agent yang berjalan di hos lain, tetapkan secret pada hos tersebut. Di Windows, buka terminal baru selepas menetapkan pemboleh ubah pengguna.

Dari root repo dalam Codespaces, selepas `bash tools/setup.sh`:

```bash
.venv/bin/python -m pip install -r requirements-ludo.txt
.venv/bin/python tools/jana_ludo.py /tmp/narasi-s01.txt /tmp/s01.wav
```

Dalam PowerShell Windows, dari root repo:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-ludo.txt
.\.venv\Scripts\python.exe tools\jana_ludo.py .\narasi-s01.txt .\s01.wav
```

Sediakan fail teks narasi UTF-8 dahulu dan pilih laluan WAV baharu. Skrip meminta model `gemini-3.8-flash-tts` dengan suara **Ludo**. SDK **2.34.0** lulus penjanaan WAV di Windows dan Codespaces. SDK 3.3.0 ditolak pada medan `speechConfig` dalam ujian Codespaces. Jika menggunakan UI, pilih Ludo dalam Google AI Studio dan simpan WAV melalui muat turun.

## Video baharu

Skill dan preset: lihat [inventori pemasangan](docs/INSTALLED-TOOLS.md).

Simpan bahan sebagai teks atau Markdown UTF-8. Arahan ini memeriksa versi tempatan dan remote, mencipta branch daripada `origin/main`, serta menyediakan storyboard yang boleh disunting:

```bash
./video new "Nama Video Saya" --source /laluan/bahan.md
# Jana dan semak WAV Ludo, simpan audio/sXX.wav serta audio/sXX.cues.json.
./video render videos/nama-video-saya/v001 --workers 2
./video publish videos/nama-video-saya/v001
```

- Branch: `video/nama-video-saya/v001`.
- Tag versi: `nama-video-saya-v001`.
- Tajuk sama pada penghasilan seterusnya mendapat `v002`, `v003` dan seterusnya.
- Tajuk lain bermula pada `v001` sendiri. Nombor tidak bergantung pada versi video lain.
- `publish` menghantar branch dan tag bersama selepas semakan, tanpa force-push. Ini menyimpan pada GitHub; ia tidak menerbitkan ke media sosial atau membuat GitHub Release.

`new` memerlukan working tree bersih dan akses baca remote. `publish` memerlukan akses tulis GitHub. Untuk video tanpa akses GitHub, folder projek yang sudah tersedia masih boleh dirender. Tiada credential disimpan dalam projek.

## Menyunting dan merender semula

Sunting `storyboard.json` dalam folder versi yang baharu: `narration` untuk suara, `title` dan `bullets` untuk visual. Selepas menukar narasi, jana semula Ludo melalui Gemini API atau UI Google AI Studio, semak rakaman serta kemas kini WAV dan cues sebelum render:

```bash
./video render videos/nama-video-saya/v001
```

`--frames-only` menggunakan audio sedia ada untuk menyediakan masa dan pratonton tanpa eksport penuh. Eksport penuh ialah H264/AAC 1280×720, 30fps, dengan muzik prosedural, SRT dan versi MP4 berkapsyen pilihan. Hash render, bilangan bingkai, tempoh, codec, loudness dan nyahkod penuh diperiksa. Semakan sebutan dan ketepatan fakta oleh manusia tetap berasingan daripada semakan teknikal.

Narasi wajib ialah Google AI Studio **Ludo**. Ikut [skill suara](.agents/skills/google-ai-studio-voiceover/SKILL.md), simpan `audio/sXX.wav` serta `audio/sXX.cues.json` dengan `narration` yang sepadan. Tiada fallback automatik. `--resynthesize` kini berhenti dengan panduan menjana semula Ludo. Rekod model dan suara daripada konfigurasi API atau pilihan suara dalam UI. Preset Full HD dibundel sebagai brief; ia belum mengubah renderer 720p ini.

MP4, sumber audio asal dan laporan disimpan pada branch video. Fail venv, model besar dan output perantaraan tidak dimuat naik. MP4 melebihi had GitHub 100 MiB ditolak oleh `publish`; gunakan Git LFS atau GitHub Releases bagi projek besar.

Lihat [struktur projek dan pemulihan](docs/WORKFLOW.md). Ujian: `.venv/bin/python -m unittest discover -s tests -v`.

## Aplikasi Google AI Studio Ludo

Integrasi Electron: `bash tools/setup-ludo.sh`, kemudian `./ludo` pada desktop yang boleh dilihat. Pilih storyboard, login Google sendiri, semak skrip dan luluskan penjanaan WAV Ludo. Fail suara sedia ada tidak ditimpa. Lihat [pemasangan, aliran penggunaan dan status audit](docs/LUDO-DESKTOP.md).

## Alat kawalan Chrome untuk Codex

Chrome DevTools MCP dan setup Windows disediakan untuk klik/taip melalui agent dalam task local. Lihat [cara mendaftar tool pada PC dan batas tab browser Codex](docs/BROWSER-CONTROL.md). Pemasangan di cloud tidak menyambungkan tab Windows secara automatik.
