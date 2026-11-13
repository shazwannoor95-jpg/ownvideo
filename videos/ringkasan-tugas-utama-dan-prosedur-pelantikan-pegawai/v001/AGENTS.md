# Syarat khusus projek ini

- Pengguna telah mengarahkan ABAIKAN PDF baharu. Sumber fakta ialah source/teks-enam-pelantikan-disahkan-pengguna.md, dengan gred 5/1 disahkan semula, dan arahan produksi source/master-prompt.md.
- Wajib Ludo melalui Google AI Studio. Jangan panggil sintesis eSpeak, jangan gunakan ./video render lalai yang akan mensintesis eSpeak jika WAV tiada. Jangan menggantikan suara tanpa izin pengguna.
- Hasil akhir mesti 300–360 saat, sasaran 330; Full HD 1920×1080, 30fps, H264/AAC; kapsyen kelihatan dan SRT berasingan. Ukur WAV sebenar dahulu.
- render_fhd.py menyediakan visual native Full HD dan proof senyap sahaja. Fail produce.py/render_video.py yang diwarisi ialah engine asas 720p; belum diadaptasi untuk eksport akhir Ludo FHD. Jangan gunakannya dan mendakwa spesifikasi akhir telah lulus.
- Projek kini DRAFT / WAITING_LUDO. Jangan tag versi sebagai siap atau panggil ./video publish sehingga semua syarat dan QA sebenar lulus. Commit/push draf kerja pada branch ini dibenarkan; final memerlukan WAV Ludo, alignment kapsyen dan adaptasi pipeline akhir.
