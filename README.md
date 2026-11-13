# ownvideo

Alat dan arkib produksi video Bahasa Melayu. Setiap video mempunyai branch dan versi sendiri yang dijana daripada tajuk.

Video pertama: [Enam Jenis Pelantikan Pegawai — BARU UiTM](https://github.com/shazwannoor95-jpg/ownvideo/tree/video/enam-jenis-pelantikan-pegawai-baru-uitm/v001).

## Pasang

Python 3.12+, FFmpeg/FFprobe dengan libx264 dan AAC, serta Git diperlukan. Pada Ubuntu/Debian, pasang pakej sistem melalui pengurus pakej yang dibenarkan oleh mesin anda. Tiada GPU, akaun Google atau API key diperlukan untuk suara Melayu luar talian.

```bash
bash tools/setup.sh
```

Pemasangan menggunakan `.venv` berasingan. Fon, ikon, logo, lesen, renderer, penjana muzik dan alat semakan dibundel dalam `tools/template/`. Ia tidak bergantung pada repo lain atau fail dalam komputer asal.

## Video baharu

Simpan bahan sebagai teks atau Markdown UTF-8. Arahan ini memeriksa versi tempatan dan remote, mencipta branch daripada `origin/main`, serta menyediakan storyboard yang boleh disunting:

```bash
./video new "Nama Video Saya" --source /laluan/bahan.md
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

Sunting `storyboard.json` dalam folder versi yang baharu: `narration` untuk suara, `title` dan `bullets` untuk visual. Selepas menukar narasi:

```bash
./video render videos/nama-video-saya/v001 --resynthesize
```

`--frames-only` menyediakan audio, masa dan pratonton tanpa eksport penuh. Eksport penuh ialah H264/AAC 1280×720, 30fps, dengan muzik prosedural, SRT dan versi MP4 berkapsyen pilihan. Hash render, bilangan bingkai, tempoh, codec, loudness dan nyahkod penuh diperiksa. Semakan sebutan dan ketepatan fakta oleh manusia tetap berasingan daripada semakan teknikal.

Narasi lalai ialah suara sintetik eSpeak NG Bahasa Melayu. Projek boleh membekalkan WAV sendiri dengan nama `audio/sXX.wav` serta `audio/sXX.cues.json` untuk kapsyen; gunakan `narration` yang sepadan. Jangan gunakan `--resynthesize` jika mahu mengekalkan suara tersebut.

MP4, sumber audio asal dan laporan disimpan pada branch video. Fail venv, model besar dan output perantaraan tidak dimuat naik. MP4 melebihi had GitHub 100 MiB ditolak oleh `publish`; gunakan Git LFS atau GitHub Releases bagi projek besar.

Lihat [struktur projek dan pemulihan](docs/WORKFLOW.md). Ujian: `.venv/bin/python -m unittest discover -s tests -v`.
