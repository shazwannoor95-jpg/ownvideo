import subprocess, concurrent.futures
from pathlib import Path
p=Path('/workspace/ownvideo/videos/pelantikan-dan-peranan-pegawai-pengurusan-rekod/v001')
def gen(i):
 s=f's{i:02}'
 r=subprocess.run(['/workspace/ownvideo/.venv/bin/python','tools/jana_ludo.py',str(p/'source'/f'{s}-narasi.txt'),str(p/'audio'/f'{s}.wav')],cwd='/workspace/ownvideo',capture_output=True,text=True)
 print(s,r.returncode,r.stdout,r.stderr[-1500:],flush=True)
 return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 results=list(ex.map(gen,range(1,9)))
print('RESULTS',results)
