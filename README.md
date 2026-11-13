# ownvideo

Alat dan arkib produksi video Bahasa Melayu. Setiap video mempunyai branch dan versi sendiri yang dijana daripada tajuk.

Video pertama: [Enam Jenis Pelantikan Pegawai — BARU UiTM](https://github.com/shazwannoor95-jpg/ownvideo/tree/video/enam-jenis-pelantikan-pegawai-baru-uitm/v001).

**[Muat turun MP4 — 13 minit 55 saat, 47 babak (36.8 MB)](https://github.com/shazwannoor95-jpg/ownvideo/raw/68aed8891e2b3d0ad330f4dd7b90d8b3e210a09b/videos/enam-jenis-pelantikan-pegawai-baru-uitm/v001/outputs/enam-jenis-pelantikan-pegawai-baru-uitm-v001-kapsyen.mp4?download=1)**

Arahan berterusan untuk agent: muat naik setiap video yang siap bersama fail kerja dan alat yang diperlukan, kemudian berikan pautan muat turun GitHub. Branch serta tag versi dijana mengikut tajuk melalui workflow di bawah. Arahan operasi disimpan dalam `AGENTS.md`.

## Pasang

Python 3.12+, FFmpeg/FFprobe dengan libx264 dan AAC, serta Git diperlukan. Pada Ubuntu/Debian, pasang pakej sistem melalui pengurus pakej yang dibenarkan oleh mesin anda. Tiada GPU diperlukan. Narasi produksi mesti menggunakan Google AI Studio dengan suara Ludo melalui akaun Google pengguna; aliran UI ini tidak memerlukan API key.

```bash
bash tools/setup.sh
```

Pemasangan menggunakan `.venv` berasingan. Fon, ikon, logo, lesen, renderer, penjana muzik dan alat semakan dibundel dalam `tools/template/`. Ia tidak bergantung pada repo lain atau fail dalam komputer asal.

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

Sunting `storyboard.json` dalam folder versi yang baharu: `narration` untuk suara, `title` dan `bullets` untuk visual. Selepas menukar narasi, jana semula Ludo melalui Google AI Studio, semak rakaman serta kemas kini WAV dan cues sebelum render:

```bash
./video render videos/nama-video-saya/v001
```

`--frames-only` menggunakan audio sedia ada untuk menyediakan masa dan pratonton tanpa eksport penuh. Eksport penuh ialah H264/AAC 1280×720, 30fps, dengan muzik prosedural, SRT dan versi MP4 berkapsyen pilihan. Hash render, bilangan bingkai, tempoh, codec, loudness dan nyahkod penuh diperiksa. Semakan sebutan dan ketepatan fakta oleh manusia tetap berasingan daripada semakan teknikal.

Narasi wajib ialah Google AI Studio **Ludo**. Ikut [skill suara](.agents/skills/google-ai-studio-voiceover/SKILL.md), simpan `audio/sXX.wav` serta `audio/sXX.cues.json` dengan `narration` yang sepadan. Tiada fallback automatik. `--resynthesize` kini berhenti dengan panduan menjana semula Ludo. WAV sendiri tidak membuktikan suara Ludo: semak sumber suara dalam UI. Preset Full HD dibundel sebagai brief; ia belum mengubah renderer 720p ini.

MP4, sumber audio asal dan laporan disimpan pada branch video. Fail venv, model besar dan output perantaraan tidak dimuat naik. MP4 melebihi had GitHub 100 MiB ditolak oleh `publish`; gunakan Git LFS atau GitHub Releases bagi projek besar.

Lihat [struktur projek dan pemulihan](docs/WORKFLOW.md). Ujian: `.venv/bin/python -m unittest discover -s tests -v`.

## Aplikasi Google AI Studio Ludo

Integrasi Electron: `bash tools/setup-ludo.sh`, kemudian `./ludo` pada desktop yang boleh dilihat. Pilih storyboard, login Google sendiri, semak skrip dan luluskan penjanaan WAV Ludo. Fail suara sedia ada tidak ditimpa. Lihat [pemasangan, aliran penggunaan dan status audit](docs/LUDO-DESKTOP.md).

## Alat kawalan Chrome untuk Codex

Chrome DevTools MCP dan setup Windows disediakan untuk klik/taip melalui agent dalam task local. Lihat [cara mendaftar tool pada PC dan batas tab browser Codex](docs/BROWSER-CONTROL.md). Pemasangan di cloud tidak menyambungkan tab Windows secara automatik.
