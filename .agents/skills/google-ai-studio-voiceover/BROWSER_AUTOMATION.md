# Automasi pelayar dan penyimpanan

## Antara muka yang digunakan

Sesi 4 November menggunakan `mcp__cua_repl.js` dan memilih tab sedia ada melalui `cua.getTab({url: URL_TAB}, {browser: 'iab'})`. Rekod 2 November turut menunjukkan laluan membuka tab melalui CUA. Untuk chat baharu, baca dokumentasi alat yang tersedia dan ambil keadaan tab semasa. Panggilan pertama tertakluk kepada arahan alat hos. `cua.rewriteDocumentation()` direkodkan ketika menyambung sesi.

Sesi asal menggunakan `getAXState()`, `paste(..., {format: 'text'})`, `setValue(...)`, `pressKey(...)`, `click(...)`, dan Playwright locator yang disediakan dalam tab CUA. Cari kawalan melalui nama yang muncul dalam keadaan tab terkini. Nombor elemen lama dan laluan profil Google berangka bergantung pada sesi. Gunakan aksi locator bersamaan jika hos menyediakan antara muka berbeza. Pemerhatian login dibuat daripada skrin Google yang memerlukan pengesahan atau editor yang boleh digunakan selepas pengguna kembali.

## Laluan WAV yang berjaya direkodkan

1. Apabila **Download** aktif, periksa pemain audio. Rekod pernah menunjukkan elemen `audio` dengan data URL tetapi tempohnya hanya **0.04 saat**. Kehadiran data URL sahaja tidak mengesahkan WAV penuh.
2. Jeda pemain jika ia sedang dimainkan. Gunakan kawalan **Seek audio position** untuk kembali ke sifar, kemudian tekan main. Pada rakaman yang disahkan, tempoh elemen menjadi **94.36 saat** dan data URL membesar dengan sepadan.
3. Baca atribut `src` hanya daripada pemain audio hasil yang dapat dikenal pasti pada tab sendiri. Sesi asal menggunakan operasi CUA berikut. Coretan ini mengandaikan ikatan `voiceTab` yang sah, folder keluaran yang boleh ditulis, dan bahawa hasil menggunakan data URL WAV. Ia ialah penyesuaian logik asal dengan semakan pengepala dan tanpa ambang saiz tetap.

```js
const player = voiceTab.playwright.locator('audio');
const src = await player.getAttribute('src');
const prefix = 'data:audio/wav;base64,';
if (!src?.startsWith(prefix)) throw new Error('WAV penuh tidak tersedia melalui pemain.');
const bytes = Buffer.from(src.slice(prefix.length), 'base64');
if (bytes.length < 44 ||
    bytes.toString('ascii', 0, 4) !== 'RIFF' ||
    bytes.toString('ascii', 8, 12) !== 'WAVE' ||
    bytes.readUInt32LE(4) + 8 !== bytes.length) {
  throw new Error('WAV kosong, rosak atau terpotong.');
}
const fs = await import('node:fs/promises');
await fs.writeFile(outputWav, bytes, {flag: 'wx'});
nodeRepl.write({bytes: bytes.length});
```

4. Sahkan tempoh WAV pada cakera dengan `ffprobe` atau Python `wave`. Bandingkan dengan tempoh pemain dan jumlah teks kelompok. Semak sampel akhir dan sebutan. Ambang 1 MB dalam rekod asal khusus untuk kelompok panjang dan boleh menolak klip pendek yang sah.
5. Jika hos mengehadkan API, pemindahan binari atau akses cakera, atau jika elemen tiada data URL WAV, gunakan fungsi muat turun hos jika tersedia. Jika fail tidak dapat disimpan atau diambil oleh hos, minta pengguna klik **Download** sendiri dan lampirkan WAV. Jangan cetak kandungan base64, butiran akaun, atau maklumat sesi ke chat.

Pengesahan akaun Google berlaku di pelayar yang pengguna kawal. Apabila sesi tamat, minta pengguna menyelesaikan pengesahan dan sahkan editor tersedia sebelum meneruskan. Akaun, kuota dan storan tab ialah keadaan hos semasa.