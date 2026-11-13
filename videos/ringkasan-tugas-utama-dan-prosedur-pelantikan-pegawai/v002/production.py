"""Resume native FHD production only after genuine Ludo WAVs, cues and review exist."""
from pathlib import Path
import argparse,hashlib,json,math,subprocess,wave
ROOT=Path(__file__).resolve().parent
FPS=30

def read(name):return json.loads((ROOT/name).read_text())
def write(name,data):
    p=ROOT/name;p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def run(args):subprocess.run([str(x) for x in args],check=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepare():
    story=read('storyboard.json');clips=[];missing=[]
    for s in story['scenes']:
        for suffix in ['.wav','.cues.json']:
            name=f"audio/{s['id']}{suffix}"
            if not (ROOT/name).is_file():missing.append(name)
    if missing:raise ValueError('WAV Ludo dan cues sebenar belum tersedia: '+', '.join(missing))
    review=read('audio/ludo-review.json')
    if review.get('provider')!='Google AI Studio' or review.get('voice')!='Ludo':raise ValueError('Semakan sumber suara Google AI Studio Ludo diperlukan.')
    total=0;timeline=[]
    for s in story['scenes']:
        sid=s['id'];wav=ROOT/f'audio/{sid}.wav'
        with wave.open(str(wav)) as w:
            if not w.getnframes() or w.getcomptype()!='NONE':raise ValueError('WAV PCM tidak sah: '+sid)
            seconds=w.getnframes()/w.getframerate()
        reviewed=review.get('clips',{}).get(sid,{})
        if (reviewed.get('audio_sha256')!=sha(wav) or reviewed.get('narration_sha256')!=hashlib.sha256(s['narration'].encode()).hexdigest()
            or reviewed.get('ui_voice_confirmed') is not True or reviewed.get('script_checked') is not True
            or reviewed.get('review_method') not in ['listening','independent_transcription']):
            raise ValueError('Semakan UI, audio dan skrip sebenar diperlukan: '+sid)
        cues=read(f'audio/{sid}.cues.json');last=0
        if not cues:raise ValueError('Cues kosong: '+sid)
        for c in cues:
            if not (0<=c['start']<c['end']<=seconds+.02 and c['start']>=last and c['text'].strip()):raise ValueError('Masa cues tidak sah: '+sid)
            last=c['end']
        frames=math.ceil((seconds+1)*FPS);duration=frames/FPS
        s.update(duration=duration,duration_frames=frames,audio_duration=seconds,narration_offset=.25)
        end=(round(total*FPS)+frames)/FPS
        timeline.append({'id':sid,'start_seconds':total,'end_seconds':end,'duration_seconds':duration,'audio_seconds':seconds})
        total=end
        clips.append({'id':sid,'audio_sha256':sha(wav),'seconds':seconds,'cues':len(cues)})
    if not 300<=total<=360:raise ValueError(f'Durasi sebenar {total:.3f}s di luar 300–360s. Laraskan skrip/tempo natural dan jana semula Ludo; jangan tambah jeda panjang atau potong dialog.')
    write('storyboard.json',story);write('timeline.json',{'scenes':timeline,'duration_seconds':total,'basis':'measured real PCM WAV + 0.25s lead + 0.75s guard'})
    write('qa/ludo-audio-check.json',{'status':'passed declared review and file integrity','voice':'Google AI Studio — Ludo','clips':clips,'actual_seconds':total,'review':review})
    print('Measured Ludo timeline:',total)

def render():
    import render_fhd as f
    f.DRAFT=False
    for i,s in enumerate(f.SCENES):
        if 'duration' not in s:raise ValueError('Jalankan --prepare dengan WAV sebenar dahulu.')
        f.encode(i,s['duration'],ROOT/'rendered'/f"{s['id']}.mp4")
        print('Rendered',s['id'],flush=True)

def assemble():
    story=read('storyboard.json');timeline=read('timeline.json');project=read('project.json')
    cache=ROOT/'rendered';cache.mkdir(exist_ok=True)
    entries=[];audio=[]
    for s in story['scenes']:
        entries.append("file '"+str(cache/f"{s['id']}.mp4")+"'\n")
        dst=cache/f"{s['id']}-aligned.wav"
        run(['ffmpeg','-v','error','-nostdin','-y','-i',ROOT/f"audio/{s['id']}.wav",'-af',f"loudnorm=I=-16:TP=-1.5:LRA=11,adelay=250:all=1,apad,atrim=duration={s['duration']},aresample=48000",'-ac','1','-c:a','pcm_s16le',dst]);audio.append(dst)
    listing=cache/'visual-concat.txt';listing.write_text(''.join(entries))
    audio_list=cache/'audio-concat.txt';audio_list.write_text(''.join(f"file '{p}'\n" for p in audio))
    mix=cache/'narration-master.wav'
    run(['ffmpeg','-v','error','-nostdin','-y','-f','concat','-safe','0','-i',audio_list,'-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-ac','1',mix])
    out=ROOT/'outputs'/f"{project['slug']}-{project['version']}.mp4"
    run(['ffmpeg','-v','error','-nostdin','-y','-f','concat','-safe','0','-i',listing,'-i',mix,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(timeline['duration_seconds']),'-movflags','+faststart',out])
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]))
    v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio');seconds=float(probe['format']['duration'])
    checks={'h264':v['codec_name']=='h264','full_hd':(v['width'],v['height'])==(1920,1080),'30fps':v['r_frame_rate']=='30/1','aac':a['codec_name']=='aac','duration_300_360':300<=seconds<=360,'measured_timing':abs(seconds-timeline['duration_seconds'])<.1}
    run(['ffmpeg','-v','error','-i',out,'-f','null','-']);checks['full_decode']=True
    write('qa/final-technical-report.json',{'technical_checks_passed':all(checks.values()),'checks':checks,'duration_seconds':seconds,'subtitles':'burned from supplied measured cues; human alignment review remains required','voice_source':'declared and hash-bound review; not machine identification of speaker'})
    if not all(checks.values()):raise ValueError('Semakan teknikal gagal.')

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','render','assemble']);a=p.parse_args()
    (ROOT/'rendered').mkdir(exist_ok=True);(ROOT/'outputs').mkdir(exist_ok=True)
    {'prepare':prepare,'render':render,'assemble':assemble}[a.action]()
if __name__=='__main__':main()
