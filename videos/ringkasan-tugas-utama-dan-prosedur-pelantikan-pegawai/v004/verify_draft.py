"""Verify the six-minute preview only; never marks missing voice as complete."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent
p=R/'outputs/DRAF_6_MINIT_MUZIK_MENUNGGU_LUDO.mp4'
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
v=[s for s in info['streams'] if s['codec_type']=='video'];a=[s for s in info['streams'] if s['codec_type']=='audio']
assert len(v)==len(a)==1
v=v[0];a=a[0]
checks={'h264':v['codec_name']=='h264','native_full_hd':(v['width'],v['height'])==(1920,1080),'fps_30':v['avg_frame_rate']=='30/1','six_minutes':abs(float(info['format']['duration'])-360)<.08,'frames_10800':int(v['nb_frames'])==10800,'aac':a['codec_name']=='aac','stereo':a['channels']==2,'sample_rate_48khz':int(a['sample_rate'])==48000}
assert all(checks.values()),checks
result=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-map','0:a:0','-f','null','-'],capture_output=True,text=True)
checks['full_decode']=result.returncode==0 and not result.stderr.strip()
assert checks['full_decode'],result.stderr
loud=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-vn','-af','volumedetect','-f','null','-'],capture_output=True,text=True,check=True)
summary=[l.strip() for l in loud.stderr.splitlines() if 'mean_volume:' in l or 'max_volume:' in l]
report={'artifact':p.name,'duration_seconds':float(info['format']['duration']),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'preview_checks':checks,'preview_technical_checks_passed':all(checks.values()),'audio_loudness':summary,'audio_content':'original instrumental music only, no speech','narration_generated':False,'narration_voice_verified':False,'caption_alignment_verified':False,'estimated_timing':True,'final_video_complete':False,'publish_ready':False,'remaining':'Google AI Studio Ludo WAVs, actual audio review, timing alignment, visible captions, final voice/music mix and final QA.'}
(R/'qa/preview-technical-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
