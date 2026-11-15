from pathlib import Path
import json,shutil,hashlib,zipfile
p=Path(__file__).resolve().parent;out=p/'outputs'
info=json.loads((p/'project.json').read_text());r=json.loads((p/'qa/final-technical-report.json').read_text())
assert r['technical_checks_passed']
assert 300<=r['duration_seconds']<=360
final=out/'Video_Pelantikan_Pegawai_UiTM_Final.mp4';shutil.copy(p/info['final_video'],final)
shutil.copy(out/'Kapsyen_BM.srt',out/'Video_Pelantikan_Pegawai_UiTM.srt')
info['final_video']=str(final.relative_to(p));info['final_sha256']=hashlib.sha256(final.read_bytes()).hexdigest();(p/'project.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
story=json.loads((p/'storyboard.json').read_text());beats=sum(len(s['visual_beats']) for s in story['scenes'])
report=f'''# Laporan QA — v003

Durasi sebenar: {r['duration_seconds']:.3f} saat ({int(r['duration_seconds']//60):02d}:{int(r['duration_seconds']%60):02d}).
Resolusi asli: 1920 × 1080. Frame rate: 30 fps. Codec: H.264 / AAC. 8 babak, 6 pelantikan, {beats} perubahan visual.

Sumber fakta: PDF pengguna dan MASTER PROMPT terkini. Pemetaan dan percanggahan sumber direkodkan dalam semakan-sumber.md. Carta alir menggunakan urutan yang dibekalkan dalam brief. Logo UiTM dan 7 Dekad diekstrak daripada PDF.

Suara sintetik Ludo dijana melalui Gemini API: gemini-3.8-flash-tts bagi s01–s03; gemini-3.8-flash-lite-tts bagi s04–s08. Model utama mencapai kuota harian; model lite menerima konfigurasi suara Ludo. Tiada suara gantian digunakan. Kawalan browser tidak tersedia.

Sari kata dibakar dalam MP4 dan disediakan sebagai SRT serta trek kapsyen. Masa dianggarkan dengan durasi WAV sebenar, kedudukan teks dan sela senyap yang diukur. Semakan ketepatan masa sari kata dan sebutan oleh manusia belum disahkan. Tiada dakwaan semakan pendengaran atau transkripsi bebas telah lulus.

Semua {len(r['checks'])} semakan teknikal lulus: codec, resolusi, fps, jumlah bingkai, durasi, audio stereo 48 kHz, aras bunyi, puncak audio dan nyahkod keseluruhan. Susun atur teks diperiksa serta pratonton setiap perubahan visual disediakan. Muzik instrumental asal dijana bagi versi ini pada aras rendah. Tiada pengesahan penerimaan undang-undang dibuat.
'''
(p/'qa/Ringkasan_QA.md').write_text(report);shutil.copy(p/'qa/Ringkasan_QA.md',out/'Ringkasan_QA.md')
with zipfile.ZipFile(out/'Bahan_Produksi_v003.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name in ['project.json','storyboard.json','timeline.json','produce.py','render_video.py','render_fhd.py','jana_ludo_lite.py','create_audio.py','finalise.py']:
  z.write(p/name,name)
 for folder in ['source','assets','local_resources','qa']:
  for f in (p/folder).rglob('*'):
   if f.is_file() and '__pycache__' not in str(f):z.write(f,str(f.relative_to(p)))
 for f in (p/'audio').glob('*'):
  if f.is_file() and (f.name.startswith('s') or f.name=='ludo-generation.json'):z.write(f,str(f.relative_to(p)))
 for name in ['Video_Pelantikan_Pegawai_UiTM.srt','skrip_narasi_bm.md','storyboard_video.md','Ringkasan_QA.md']:z.write(out/name,name)
print(report,flush=True)
