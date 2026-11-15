# Menyambung produksi: Ludo wajib

616 perkataan, 8 babak; bajet awal 330 saat. Draf visual 330s tidak mengandungi audio dan bukan MP4 akhir. Masa sebenar akan ditentukan oleh WAV; pipeline menolak durasi akhir di luar 300–360 saat. Skrip mungkin perlu dipendekkan atau dilengkapkan selepas ukuran sebenar, tanpa jeda panjang atau mempercepat suara secara keterlaluan.

## Jana dan serahkan WAV

1. Buka https://aistudio.google.com/generate-speech. Kendalikan login/pengesahan Google sendiri.
2. Speaker: pilih **Ludo** dan semak label semasa. Mulakan dengan klip ujian pendek.
3. Medan Style: “Baca dalam Bahasa Melayu Malaysia baku. Gunakan nada narator latihan korporat yang jelas, tenang dan yakin. Ikut skrip dengan tepat. Beri jeda natural dan sebut akronim, nama serta kod mengikut bentuk sebutan yang ditulis.”
4. Speech block text: tampal kandungan `source/narasi_s01.txt` sahaja. Run, tunggu Download aktif dan semak audio penuh. Ulang untuk `s02` hingga `s08`. Jangan hantar logo, dokumen atau arahan produksi ke Google.
5. Namakan muat turun seperti dalam `skrip_narasi_bm.md`, kemudian padankan kepada `audio/s01.wav` hingga `audio/s08.wav`. WAV boleh juga dilampirkan dalam chat untuk disambung; jangan ubah atau mengganti suara secara automatik.
6. Semak sebutan, kelengkapan ayat, nama, kod dan akronim melalui pendengaran atau transkripsi bebas. Sediakan `audio/sXX.cues.json` berdasarkan masa sebenar, bukan anggaran perkataan. Format: `[{"start":0.0,"end":2.5,"text":"Teks yang benar-benar dibaca"}]`. Masa relatif kepada WAV adegan, tanpa offset video. Pecahkan kepada cue pendek yang boleh dipaparkan dalam dua baris.

## Rekod semakan dan render akhir

Hanya selepas semakan sebenar, simpan `audio/ludo-review.json`:

```json
{
  "provider": "Google AI Studio",
  "voice": "Ludo",
  "clips": {
    "s01": {
      "ui_voice_confirmed": true,
      "script_checked": true,
      "review_method": "listening",
      "audio_sha256": "HASH_WAV_SEBENAR",
      "narration_sha256": "HASH_UTF8_NARRATION_DALAM_STORYBOARD_JSON"
    }
  }
}
```

Lengkapkan semua `s01`–`s08`. Kaedah alternatif: `independent_transcription`. Jangan tandakan semakan yang belum dilakukan. Hash mengikat rekod kepada fail; hash dan metadata tidak mengenal pasti suara secara automatik.

Dari akar repo, selepas input tersedia:

```bash
.venv/bin/python videos/ringkasan-tugas-utama-dan-prosedur-pelantikan-pegawai/v002/finalise.py
```

Ini menggunakan pipeline **khusus versi** Full HD: ukur PCM, tambah 0.25s lead dan 0.75s guard, kuatkuasakan had 300–360s, render kapsyen pada bingkai, seimbangkan audio, eksport H264/AAC, nyahkod penuh dan eksport nama fail yang diminta. Jika durasi di luar had, laraskan skrip dan jana semula Ludo terlebih dahulu. Susunan beat visual masih perlu disemak terhadap frasa sebenar sebelum penerimaan akhir.

Pipeline final belum dijalankan dengan rakaman Ludo sebenar. Semakan fixture sintetik hanya menguji logik masa, penolakan input rosak dan susun atur kapsyen. Selepas render sebenar, semak audio, visual, semua sempadan babak, sari kata dan laporan QA; barulah jalankan `./video publish videos/ringkasan-tugas-utama-dan-prosedur-pelantikan-pegawai/v002`.

## Halangan semasa

Permintaan HTTPS ke `aistudio.google.com` ditolak proksi dengan CONNECT 403; Chromium/Playwright mengembalikan `ERR_TUNNEL_CONNECTION_FAILED`. Tiada pilihan Ludo, kuota, login atau WAV dapat disahkan. Alat CUA/desktop hos khusus tidak ditawarkan dalam sesi ini.

Draf domain akses sudah disediakan dalam tetapan persekitaran: `aistudio.google.com`, `accounts.google.com`, `www.gstatic.com`, `ssl.gstatic.com`. Semak dan simpan tetapan, kemudian Publish untuk tugas seterusnya. Selepas perubahan berkuat kuasa, akses perlu diuji semula. Alternatifnya, jana WAV Ludo di pelayar sendiri dan lampirkan semua klip.

Logo UiTM asal digunakan semula; logo 7 Dekad berasingan tidak tersedia dalam templat yang dibekalkan, jadi tiada logo rekaan digunakan.
