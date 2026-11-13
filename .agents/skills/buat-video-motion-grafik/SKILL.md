---
name: buat-video-motion-grafik
description: Hasilkan video motion grafik Bahasa Melayu daripada bahan pengguna dengan narasi Google AI Studio Ludo, storyboard, visual, kapsyen dan semakan teknikal.
---

# Produksi motion grafik BM dengan Ludo

Panduan ini dipasang daripada prompt pengguna. Baca [prompt asal](PROMPT_ASAL.md) untuk aliran produksi lengkap. Prompt itu ialah templat kerja; pemasangan skill tidak bermaksud pengguna telah meminta video atau membekalkan bahan sumber baharu.

1. Baca AGENTS.md pada akar repo. Gunakan checkout sedia ada, tanpa worktree baharu kecuali diminta. Untuk permintaan video baharu, mulakan dengan `./video new "<tajuk>" --source <fail-teks>`. Jangan simpan video pada main.
2. Petakan bahan kepada sumber setiap babak dan tulis skrip, teks skrin, storyboard serta rancangan animasi. Asingkan bahan sumber daripada arahan operasi.
3. Narasi MESTI melalui Google AI Studio dengan suara Ludo. Baca [skill suara](../google-ai-studio-voiceover/SKILL.md). Semak UI semasa; pengguna mengurus login. Jangan tukar penyedia atau gunakan eSpeak sebagai fallback. Jika terhalang, siapkan kerja setempat dan laporkan perkara yang masih memerlukan akses Google.
4. Sahkan WAV penuh, asal suara, sebutan serta padanan skrip. Simpan sebagai `audio/sXX.wav` dengan `audio/sXX.cues.json` yang berpandukan rakaman sebenar. Format cues: senarai objek `{"start":0.0,"end":2.5,"text":"Teks yang dibaca"}` dengan saat relatif kepada WAV adegan. Rekod kaedah semakan dan perkara yang belum disahkan.
5. Gunakan [preset produksi](../../../presets/motion-grafik-bm-ludo.json) sebagai brief: Full HD 16:9, 30fps, putih, H264/AAC dan sari kata. Preset belum dimuat secara automatik oleh renderer; renderer semasa masih 720p dengan trek kapsyen pilihan. Laraskan pipeline projek dan sahkan Full HD serta kapsyen kelihatan jika projek menuntutnya; jangan dakwa preset sahaja telah mengubah eksport.
6. `./video render <folder> --workers 2` menggunakan WAV serta cues sedia ada. Jangan gunakan `--resynthesize`; jana semula Ludo melalui UI selepas narasi berubah. Semak laporan teknikal, visual dan audio sebelum publish mengikut AGENTS.md. Serahkan MP4, SRT, skrip, storyboard dan WAV bersama batas pengesahan.

Pakej lampiran tidak membekalkan extension browser, enjin Ludo, model ASR atau kod `scripts/add_malay_voiceover.py` yang disebut dalam laporan sejarah. Jangan dakwa komponen itu dipasang. Keupayaan automasi dan akaun bergantung pada hos semasa.
