from pathlib import Path
import subprocess,time
p=Path('/workspace/ownvideo/videos/ringkasan-tugas-utama-dan-prosedur-pelantikan-pegawai/v003')
for i in range(1,9):
 sid=f's{i:02}';out=p/'audio'/f'{sid}.wav'
 if out.exists():continue
 for attempt in range(5):
  r=subprocess.run(['/workspace/ownvideo/.venv/bin/python','videos/ringkasan-tugas-utama-dan-prosedur-pelantikan-pegawai/v003/jana_ludo_lite.py',str(p/'source'/f'{sid}-narasi.txt'),str(out)],cwd='/workspace/ownvideo',capture_output=True,text=True)
  if not r.returncode:print(r.stdout,flush=True);break
  if 'per day' in r.stderr:print(r.stderr[-2200:],flush=True);raise RuntimeError('Kuota harian model ini telah habis')
  if '429' not in r.stderr:print(r.stderr[-1800:],flush=True);raise RuntimeError(sid)
  print(sid,'had sementara; cuba semula dalam 30 saat',flush=True);time.sleep(30)
 else:raise RuntimeError(sid)
