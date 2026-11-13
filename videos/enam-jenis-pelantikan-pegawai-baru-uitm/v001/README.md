# Enam Jenis Pelantikan Pegawai — BARU UiTM

Video: **13 minit 55 saat**, 47 babak, 1280×720 30fps, H264/AAC, narasi sintetik Melayu, muzik prosedural, kapsyen pilihan dan 9 penanda bab.

Hasil akhir berada di `outputs/` bersama SRT, skrip, teks asal, pratonton dan laporan semakan.
Sumber suara asal bagi semua 47 babak dikekalkan dalam `audio/`. Model atau akaun luar tidak diperlukan.

Dari root repo selepas `bash tools/setup.sh`:

```bash
./video render videos/enam-jenis-pelantikan-pegawai-baru-uitm/v001 --workers 2
```

Ini menghasilkan semula semua perantaraan dan video daripada storyboard serta WAV asal.
Jangan gunakan `--resynthesize` jika mahu mengekalkan suara yang telah dimuat naik.
Untuk pindaan, cipta versi seterusnya dengan tajuk yang sama melalui `./video new` dan bawa storyboard/aset yang diperlukan ke versi baharu; jangan menimpa tag versi ini.

Kesemua 11 semakan teknikal asal lulus. Laporan sejarah mengandungi laluan mesin asal sebagai provenance; arahan penyediaan menghasilkan laluan semasa secara automatik. Semakan manusia terhadap sebutan atau pengesahan undang-undang tidak didakwa selesai. Nota aliran khusus yang belum disahkan dikekalkan daripada teks sumber.
