# Struktur dan pemulihan

`main` menyimpan alat bersama, templat dan ujian. Setiap branch `video/<slug>/vNNN` bermula daripada main dan membawa satu projek di `videos/<slug>/vNNN/`. Tag `<slug>-vNNN` merujuk commit video itu. Video berlainan tidak perlu digabungkan ke main untuk disimpan.

```text
videos/<slug>/vNNN/
  project.json            # tajuk, versi, branch, tag, hash hasil
  source/                 # teks rujukan pengguna
  storyboard.json         # narasi dan reka bentuk babak
  audio/sXX.wav           # klip suara asal yang dikekalkan
  audio/sXX.cues.json      # cap masa sebenar kapsyen
  assets/, local_resources/ # aset, fon, lesen
  produce.py, render_video.py, create_audio.py
  timeline.json, video-manifest.json
  qa/                     # bukti semakan
  outputs/                # MP4, SRT, skrip dan laporan akhir
```

Selepas clone, jalankan `bash tools/setup.sh`, kemudian checkout branch video untuk mendapatkan projek dan MP4. `./video render <folder>` membina semula output perantaraan yang tidak disimpan. Folder kerja lama komputer asal tidak diperlukan. Laluan mutlak dalam laporan sejarah ialah provenance sahaja; `produce.py --prepare` menjana laluan dan hash semasa sebelum assembly.

Semua aset yang diperlukan untuk video pertama dibundel, termasuk logo UiTM, ikon dan fon Outfit dengan lesen berkaitan. Nota sumber dan penggunaan jenama dikekalkan; tiada dakwaan bahawa logo atau bahan sumber adalah domain awam.

Narasi produksi mesti Google AI Studio Ludo. Sediakan WAV dan cues yang telah disemak sebelum render; tiada fallback eSpeak automatik. Panduan dan preset baharu ada dalam [inventori pemasangan](INSTALLED-TOOLS.md).

Pipeline menjana muzik sendiri. Model Whisper, browser, Electron dan pek skill lain tidak diperlukan untuk menghasilkan video ini. Arkib asal yang dimuat naik tidak membundel definisi SKILL.md atau extension; repo ini tidak mendakwa memasang pek tersebut.

Video pertama menggunakan teks pengguna yang meliputi keenam-enam pelantikan. Hasil asal 47 babak dan 834.633 saat serta laporan semakan disertakan. Fail MP4 akhir mengandungi kapsyen pilihan dan sembilan penanda bab; fail SRT berasingan tersedia. Arahan render baharu menghasilkan MP4 serta MP4 berkapsyen; pembinaan bab khusus video asal turut disertakan sebagai skrip provenance.
