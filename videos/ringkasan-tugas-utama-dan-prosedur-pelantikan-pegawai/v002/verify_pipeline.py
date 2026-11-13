"""Synthetic test fixtures only. Does not contact Google or validate a real Ludo voice."""
from pathlib import Path
import hashlib,json,tempfile,wave
import production
import render_fhd

def fixture(root,seconds):
    (root/'audio').mkdir(exist_ok=True);review={'provider':'Google AI Studio','voice':'Ludo','clips':{}}
    story={'scenes':[]}
    for i in range(8):
        sid=f's{i+1:02}';s={'id':sid,'narration':'Test fixture only'};story['scenes'].append(s)
        wav=root/'audio'/f'{sid}.wav'
        with wave.open(str(wav),'wb') as w:
            w.setnchannels(1);w.setsampwidth(2);w.setframerate(8000);w.writeframes(bytes(round(seconds*8000)*2))
        (root/'audio'/f'{sid}.cues.json').write_text(json.dumps([{'start':0,'end':seconds,'text':'Test fixture only'}]))
        review['clips'][sid]={'audio_sha256':hashlib.sha256(wav.read_bytes()).hexdigest(),'narration_sha256':hashlib.sha256(s['narration'].encode()).hexdigest(),'ui_voice_confirmed':True,'script_checked':True,'review_method':'listening'}
    (root/'storyboard.json').write_text(json.dumps(story));(root/'audio/ludo-review.json').write_text(json.dumps(review))

def main():
    old=production.ROOT
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);production.ROOT=root
            fixture(root,40.25);production.prepare()
            assert abs(json.loads((root/'timeline.json').read_text())['duration_seconds']-9904/30)<1e-6
            (root/'audio/s01.wav').write_bytes(b'bad')
            try:production.prepare()
            except (ValueError,EOFError,wave.Error):pass
            else:raise AssertionError('Corrupt WAV accepted')
            fixture(root,45)
            try:production.prepare()
            except ValueError as exc:assert '300–360' in str(exc)
            else:raise AssertionError('Overlength accepted')
            fixture(root,2)
            try:production.prepare()
            except ValueError as exc:assert '300–360' in str(exc)
            else:raise AssertionError('Underlength accepted')
    finally:production.ROOT=old
    render_fhd.DRAFT=False
    render_fhd.captions=lambda i:[{'start':0,'end':1,'text':'UJIAN SUSUN ATUR KAPSYEN. BUKAN RAKAMAN LUDO.'}]
    assert render_fhd.frame(0,.5,15).size==(1920,1080)
    print('PASS: synthetic 330.133s timeline; corrupt WAV, under/over duration rejection; FHD caption rendering. No real Ludo tested.')
if __name__=='__main__':main()
