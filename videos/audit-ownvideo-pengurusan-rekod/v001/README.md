# Audit ownvideo dari PDF hingga MP4

- Input: PDF ujian satu halaman, dua bahagian yang diekstrak ke Markdown UTF-8 dan dijadikan storyboard dua babak.
- Narasi: dua rakaman Ludo baharu melalui Gemini API, model `gemini-3.8-flash-tts`, SDK `google-genai==2.34.0`. Lihat `qa/ludo-api.json` untuk durasi dan hash WAV.
- Output: MP4 9.667 saat, 1280×720, 30 fps, H.264 dan AAC, trek sari kata Bahasa Melayu `mov_text`, serta SRT berasingan.
- Semakan: 11 pemeriksaan teknikal lulus, kedua-dua trek utama dinyahkod penuh, sampel visual kedua-dua babak diperiksa, dan lima ujian regresi lulus. Cue meliputi tempoh WAV sebenar bagi setiap ayat. Sebutan belum disahkan oleh pendengar manusia.
- Hos: render audit ini dijalankan di Windows. Penjanaan Ludo sudah diuji berasingan di Codespaces.
- Publish: arahan publish mengesahkan branch dan tag pada remote Git tempatan. Fail projek ini diterbitkan ke GitHub melalui connector.
- Pembetulan pipeline: templat menggunakan penyedia dan suara dalam project.json, output teks ditulis sebagai UTF-8, dan pemeriksaan nyahkod akhir menghentikan proses jika FFmpeg mengesan ralat.
