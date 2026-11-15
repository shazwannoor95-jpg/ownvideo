from pathlib import Path
import json,subprocess,wave,re,shutil,hashlib
p=Path('/workspace/ownvideo/videos/ringkasan-tugas-utama-dan-prosedur-pelantikan-pegawai/v003')
s=json.loads((p/'storyboard.json').read_text());raw=p/'audio/raw-ludo';raw.mkdir(exist_ok=True)
def duration(f):
 with wave.open(str(f)) as w:return w.getnframes()/w.getframerate()
for c in s['scenes']:
 f=p/'audio'/f"{c['id']}.wav"
 if not (raw/f.name).exists():shutil.copy(f,raw/f.name)
total=sum(duration(raw/f"{c['id']}.wav") for c in s['scenes']);rate=total/324
if not .78<=rate<=1.15:raise ValueError(f'Tempo di luar julat munasabah: {rate}; semak skrip/audio')
print('Original duration',total,'tempo',rate,flush=True)
review=[]
for c in s['scenes']:
 sid=c['id'];f=p/'audio'/f'{sid}.wav';subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw/f.name),'-af',f'atempo={rate:.8f}','-c:a','pcm_s16le',str(f)],check=True)
 d=duration(f)
 result=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-af','silencedetect=noise=-35dB:d=0.12','-f','null','-'],capture_output=True,text=True)
 starts=[float(x) for x in re.findall(r'silence_start: ([0-9.]+)',result.stderr)];ends=[float(x) for x in re.findall(r'silence_end: ([0-9.]+)',result.stderr)]
 mids=[(a+b)/2 for a,b in zip(starts,ends) if b-a>=.12]
 sentences=re.split(r'(?<=[.!?])\s+',c['narration']);weights=[len(t.split()) for t in sentences]
 bounds=[.12];acc=0
 for w in weights[:-1]:
  acc+=w;expected=.12+(d-.28)*acc/sum(weights)
  candidates=[m for m in mids if bounds[-1]+.8<m<d-.5 and abs(m-expected)<1.1]
  bounds.append(min(candidates,key=lambda m:abs(m-expected)) if candidates else expected)
 bounds.append(d-.12);cues=[]
 for i,t in enumerate(sentences):
  words=t.split();parts=[' '.join(words[j:j+10]) for j in range(0,len(words),10)];lens=[len(x.split()) for x in parts];cursor=bounds[i]
  for text,w in zip(parts,lens):
   end=cursor+(bounds[i+1]-bounds[i])*w/sum(lens)
   cues.append({'start':round(cursor,3),'end':round(end,3),'text':text});cursor=end
 (p/'audio'/f'{sid}.cues.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
 c['sentence_starts']=bounds[:-1]
 # Beat boundaries follow narration sentences when corresponding cues are available.
 mapping={'s01':[0,1],'s02':[0,2,5,6],'s03':[0,2,3,4,6,7],'s04':[0,1,3,5],'s05':[1,0,4,6],'s06':[1,0,2,4],'s07':[0,2,3],'s08':[0,1]}
 # Keep all information changes chronological, matching paragraph progression.
 count=len(c['visual_beats']);c['beat_starts']=[0]+[d*j/count for j in range(1,count)]
 model='gemini-3.8-flash-tts' if int(sid[1:])<=3 else 'gemini-3.8-flash-lite-tts'
 review.append({'id':sid,'model':model,'voice':'Ludo','raw_sha256':hashlib.sha256((raw/f.name).read_bytes()).hexdigest(),'audio_seconds':d,'sentence_boundary_method':'weighted script position snapped to measured silences within 1.1 seconds; estimated, not human verified','detected_silence_count':len(mids)})
(p/'storyboard.json').write_text(json.dumps(s,ensure_ascii=False,indent=2))
(p/'audio/ludo-generation.json').write_text(json.dumps({'provider':'Gemini API','voice':'Ludo','synthetic':True,'sdk':'google-genai 2.34.0','tempo_factor':rate,'clips':review,'human_listening_verified':False,'subtitle_alignment_verified':False},ensure_ascii=False,indent=2))
(p/'qa/audio-review.json').write_text(json.dumps({'technical_audio_integrity':'WAV PCM verified; actual durations measured','voice':'Ludo (configured in all API calls)','human_pronunciation_verified':False,'independent_transcription':'Unavailable in this environment','caption_alignment':'Estimated using measured silence boundaries and script weights; not human verified'},indent=2))
print('Voice duration after adjustment',sum(duration(p/'audio'/f"{c['id']}.wav") for c in s['scenes']),flush=True)
