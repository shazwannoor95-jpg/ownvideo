# Laporan bukti pemulihan

Audit menggunakan rekod tindakan dan hasil berpasangan mengikut ID panggilan. Nombor di bawah ialah baris JSONL fizikal. Untuk menjaga privasi, rujukan sesi menggunakan tarikh dan cap masa fail. Pakej membawa ringkasan dapatan dan petunjuk semakan setempat.

- **A** — rollout 4 November 2026, 10:43:21, akhiran penanda `8a06`.
- **B** — rollout 4 November 2026, 10:43:30, akhiran penanda `af37`.
- **C** — rollout 2 November 2026, 07:30:57, akhiran penanda `ad2f`.

| Langkah | Tahap | Rekod |
|---|---|---|
| Alat browser sebenar | Disahkan | A/B 25–28: `mcp__cua_repl.js`, `cua.rewriteDocumentation()`, `cua.getTab` memilih browser `iab`. |
| Akses Generate Speech | Disahkan | A/B 27–31: sambung tab sedia ada dan periksa editor. C 174–175 menunjukkan laluan pembukaan tab dan skrin pengesahan Google; 263–264 kembali ke editor. |
| Kesan login | Disahkan melalui UI | C 175 memaparkan cabaran pengesahan dan C 264 memaparkan editor dengan kawalan pertuturan dan Run. A/B 28–31 menunjukkan editor yang tersedia. Tiada bukti audit terhadap mekanisme dalaman pengesahan Google. |
| Masukkan skrip, suara dan gaya | Disahkan | A/B 32–44: pemilihan Ludo, bacaan fail teks melalui Node, tampal teks, medan Speech block text dan tetapan Style. |
| Mulakan penjanaan | Disahkan | A/B 45–46 dan 165–166: klik kawalan UI, Stop muncul dan Download dinyahdayakan. |
| Kesan klip siap | Disahkan | A/B 65–68: Download aktif tetapi pemain mula-mula mendedahkan 0.04 s sahaja. A/B 77–78: selepas seek ke awal dan main, pemain menunjukkan 94.36 s dengan data URL penuh. |
| Muat turun melalui butang | Tindakan disahkan; fail daripada klik belum disahkan | A/B 72–73: Download diklik dan mendapat fokus. Bukti fail yang boleh dijejak datang daripada operasi penyimpanan WAV berasingan. |
| Simpan WAV setempat | Disahkan | A/B 80–81, 110–111, 139–140, 186–187: baca `audio.src` melalui locator, dekod base64 dengan Node dan tulis WAV. Hasil kelompok 2 ialah 4,529,324 bait; kelompok 5 ialah 3,331,244 bait. |
| Gunakan audio dalam video | Disahkan | A 459–485: proses Python memilih dan menyambung sampel pada sela senyap; A 506–510: 18 hash audio aktif disahkan. B 476 menerangkan kod penyediaan audio dan FFmpeg; B 602 dan 659 merekodkan MP4 akhir dan 11 semakan teknikal lulus untuk 18 adegan, 294.867 saat. Bukti teknikal tidak menyamai pengesahan setiap sebutan oleh pendengar. |

Dua log utama mengandungi rentetan panggilan pelayar yang berulang. Bukti tersebut menerangkan satu aliran yang dikongsi, bukan dua penjanaan bebas. Rekod 2 November memberi bukti tambahan bagi keadaan login dan editor. Semakan 6 dan 11 November digunakan sebagai carian silang; tuntutan utama di atas bersandar pada pasangan panggilan dan hasil A–C. Audit ini tidak membuka laman Google, membuat login atau menjana audio.