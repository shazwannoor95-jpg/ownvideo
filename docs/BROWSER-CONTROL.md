# Kawalan browser untuk Codex

Alat rasmi yang disediakan: **Chrome DevTools MCP 1.13.0**, dengan CLI `chrome-devtools`. Ia menyediakan snapshot halaman, klik, isi medan, screenshot dan penilaian JavaScript.

## Batas sambungan

Browser dalam tab aplikasi Codex yang sedang dibuka pengguna tidak semestinya Chrome yang mempunyai endpoint debugging. Pakej MCP ini tidak secara automatik menyambung kepada tab terbina dalam tersebut. Sesi cloud ini juga tidak boleh mengubah config atau menjalankan program pada PC Windows pengguna secara terus.

Laluan yang disediakan di sini ialah **Codex local → Chrome DevTools MCP local → tetingkap Chrome local**. Chrome itu akan dibuka oleh MCP apabila alat browser dipanggil. Pengguna login Google sendiri di tetingkap Chrome tersebut. Login di tab terbina dalam Codex tidak dikongsi secara automatik. Jangan salin cookie/token untuk menyambungkannya.

## Windows — setup sekali pada PC yang menjalankan Codex

1. Pastikan Node.js 24 LTS, npm dan Chrome Stable tersedia.
2. Muat turun repo ownvideo daripada main, atau kemas kini checkout sedia ada selepas menyimpan kerja anda.
3. Buka PowerShell pada folder repo dan jalankan:

```powershell
.\tools\setup-browser-control.ps1
```

Skrip menyemak pemasangan server rasmi yang dipinkan, mencari Chrome, membuat backup jika config sedia ada, lalu menambah `[mcp_servers.chrome-devtools]` ke config **PC setempat** (`CODEX_HOME/config.toml` jika dikonfigurasi, jika tidak `%USERPROFILE%\.codex\config.toml`). Ia tidak mengganti bahagian lain atau menimpa entri chrome-devtools sedia ada. Jika polisi Windows menyekat fail skrip yang dimuat turun, jangan ubah polisi keselamatan secara membuta tuli; konfigurasi contoh boleh dimasukkan secara manual oleh pengguna melalui mekanisme MCP yang disokong Codex.

4. Tutup dan buka semula Codex. Mulakan task **local** dalam repo ini, bukan chat setup cloud. Konfigurasi PC tidak dibekalkan secara automatik kepada chat cloud.
5. Minta:

> Gunakan chrome-devtools untuk list_pages dan buka https://aistudio.google.com/generate-speech. Beri saya kawalan untuk login Google sendiri. Selepas saya selesai, semak editor dan suara Ludo sebelum menghantar narasi pelantikan.

Sebelum meneruskan, agent mesti mengesahkan tool MCP `list_pages`, `new_page`, `take_snapshot`, `click` dan `fill` benar-benar tersedia. Jika tool belum muncul, konfigurasi sahaja belum membuktikan sambungan aktif. Jika ada prompt kepercayaan/kelulusan MCP daripada Codex, pengguna mengendalikannya.

Contoh config: `browser-control/codex-windows.example.toml`. GUI menu boleh berbeza mengikut versi Codex. Skrip PowerShell belum dijalankan pada Windows dalam sesi Linux ini; statusnya disediakan, bukan pemasangan PC yang disahkan.

## Linux cloud — CLI sudah dipasang dan diuji

```bash
bash tools/setup-browser-control.sh
browser-control/node_modules/.bin/chrome-devtools --help
```

Untuk ujian pada Chromium mesin ini, daemon dimulakan dalam mod tanpa paparan dengan executable khusus, profil ujian berasingan dan akses fail terhad kepada `.cache/browser-control`. Chromium ini ialah sasaran ujian; sokongan rasmi upstream ialah Google Chrome/Chrome for Testing. CLI tidak didaftarkan sebagai tool MCP perbualan ini secara automatik. `chrome-devtools stop` menghentikan daemon yang dimulakan untuk ujian.

Keputusan sebenar: pelayar membuka fixture HTTP setempat, snapshot menemui medan dan butang, `fill` mengisi `Pelantikan UiTM`, `click` menekan `Sahkan`, snapshot seterusnya menunjukkan `BERJAYA: Pelantikan UiTM`. Ini membuktikan klik/taip pada browser ujian yang dikawal CLI, bukan akses kepada tab Windows pengguna atau login Google. Tiada narasi atau credential dihantar ke Google dalam ujian ini.

Pengumpulan usage statistics dan performance CrUX dimatikan dalam konfigurasi. Tiada port debugging dibuka kepada Internet, tiada TLS/checksum dimatikan, dan profil/cookie tidak dimasukkan ke Git.

## Rujukan rasmi

- https://github.com/ChromeDevTools/chrome-devtools-mcp
- https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/client-configurations.md (bahagian Codex)
- https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/cli.md
