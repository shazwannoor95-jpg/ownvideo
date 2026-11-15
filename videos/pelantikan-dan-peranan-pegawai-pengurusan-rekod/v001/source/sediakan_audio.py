import json,wave,subprocess,math,shutil,re,hashlib
from pathlib import Path
p=Path('/workspace/ownvideo/videos/pelantikan-dan-peranan-pegawai-pengurusan-rekod/v001')
story=json.loads((p/'storyboard.json').read_text());raw=p/'audio/raw-ludo';raw.mkdir(exist_ok=True)
def dur(f):
 with wave.open(str(f)) as w:return w.getnframes()/w.getframerate()
for s in story['scenes']:
 f=p/'audio'/f"{s['id']}.wav"
 if not (raw/f.name).exists():shutil.copy(f,raw/f.name)
total=sum(dur(raw/f"{s['id']}.wav") for s in story['scenes'])
rate=total/(330-8*.75)
print('Original',total,'rate',rate,flush=True)
for s in story['scenes']:
 sid=s['id'];f=p/'audio'/f'{sid}.wav'
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw/f.name),'-af',f'atempo={rate:.8f}','-c:a','pcm_s16le',str(f)],check=True)
 d=dur(f)
 # Estimate short subtitle intervals from actual WAV length and word weights.
 # These are estimates, not verified forced alignment.
 chunks=[]
 for sent in re.split(r'(?<=[.!?])\s+',s['narration']):
  words=sent.split()
  for j in range(0,len(words),11):chunks.append(' '.join(words[j:j+11]))
 weights=[len(c.split()) for c in chunks];cursor=.12;cues=[]
 for c,w in zip(chunks,weights):
  end=cursor+(d-.28)*w/sum(weights)
  cues.append({'start':round(cursor,3),'end':round(min(d,end),3),'text':c});cursor=end
 (p/'audio'/f'{sid}.cues.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
 s['captions']=cues
(p/'storyboard.json').write_text(json.dumps(story,ensure_ascii=False,indent=2))
manifest={'provider':'Gemini API','model':'gemini-3.8-flash-tts','voice':'Ludo','sdk':'google-genai 2.34.0','synthetic_voice':True,'tempo_adjustment':rate,'target_seconds':330,'human_listening_verified':False,'caption_alignment':'Estimated from actual recording durations and script word weights; not human verified.','independent_asr':'Unavailable: model download blocked by HTTP 403.'}
(p/'audio/ludo-generation.json').write_text(json.dumps(manifest,indent=2))
(p/'qa/semakan-kandungan.md').write_text('''# Semakan kandungan dan batas pengesahan

Sumber tunggal: PDF pengguna, enam halaman. Semua peranan, gred, kuasa, borang dan tempoh dalam skrip dipetakan kepada halaman dalam storyboard. Logo diekstrak daripada halaman 5 PDF; ikon repo tidak digunakan dalam visual.

Catatan sumber: Halaman 2 memberi kuasa Pegawai Pengelas Semula secara terus di bawah seksyen 2C. Halaman 3 turut menyebut borang permohonan pelantikan dan perakuan Menteri. Ringkasan mengekalkan penerangan kuasa pada halaman 2, tanpa mereka aliran permohonan baharu. Sumber juga memaparkan label SULIT pada halaman 4; bahan sumber dikekalkan setempat dan tidak diterbitkan.

Narasi sintetik Ludo dijana dengan persetujuan pengguna. Audio diperiksa dari segi format, tempoh, kelengkapan PCM dan aras bunyi. Semakan pendengaran manusia, ketepatan sebutan dan penjajaran sari kata belum disahkan. Model transkripsi setempat tidak dapat dimuat turun (HTTP 403). Masa sari kata ialah anggaran menggunakan tempoh audio sebenar dan panjang teks. Semakan teknikal tidak mengesahkan penerimaan undang-undang.

Arahan tidak menerbitkan dipatuhi: tiada publish atau push.
''')
print('READY',sum(dur(p/'audio'/f"{s['id']}.wav") for s in story['scenes'])+6,flush=True)
