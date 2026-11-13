"""Editable native FHD motion draft. Estimated timing; no narration is synthesized."""
from pathlib import Path
from functools import lru_cache
import argparse,json,math,subprocess
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
W,H,FPS=1920,1080,30
DRAFT=True
BLUE='#042E6F';PURPLE='#92278F';GOLD='#FEBE10'
SCENES=json.loads((ROOT/'storyboard.json').read_text())['scenes']
@lru_cache(None)
def font(size):
    f=ImageFont.truetype(str(ROOT/'local_resources/Outfit[wght].ttf'),size)
    f.set_variation_by_axes([500])
    return f
@lru_cache(None)
def wrap(value,size,width):
    lines=[];line=''
    for word in value.split():
        test=(line+' '+word).strip()
        if line and font(size).getlength(test)>width:lines.append(line);line=word
        else:line=test
    if line:lines.append(line)
    return lines
AUDIT=[]
def text(im,value,xy,size=36,width=1500,fill=BLUE,maxbottom=980):
    draw=ImageDraw.Draw(im)
    lines=wrap(value,size,width)
    for i,line in enumerate(lines):draw.text((xy[0],xy[1]+i*math.ceil(size*1.25)),line,font=font(size),fill=fill,anchor='lt')
    box=[xy[0],xy[1],xy[0]+max((font(size).getlength(line) for line in lines),default=0),xy[1]+len(lines)*math.ceil(size*1.25)]
    assert box[0]>=0 and box[2]<=W and box[1]>=0 and box[3]<=maxbottom,(value,box)
    AUDIT.append({'text':value,'bounds':box,'font':size})
@lru_cache(None)
def logo():
    image=Image.open(ROOT/'assets/brand/LogoUiTM.png').convert('RGBA');image.thumbnail((270,138));return image
@lru_cache(None)
def slide(index,beat):
    s=SCENES[index];im=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(im)
    d.rectangle((0,0,18,H),fill=PURPLE)
    d.polygon([(1770,250),(W,205),(W,H),(1845,H)],fill='#F8F4FA')
    im.paste(logo(),(1590,30),logo())
    text(im,'BARU  /  UNIVERSITI TEKNOLOGI MARA',(76,42),23,1450,PURPLE)
    title=s['chapter'];size=46
    while len(wrap(title,size,1460))>1:size-=1
    text(im,title,(76,116),size,1460)
    text(im,s['title'],(76,184),28,1450,'#526885')
    for j,label in enumerate(s['visual_beats'][beat]):
        y=295+j*190
        d.rounded_rectangle((76,y,1805,y+156),radius=22,fill='#F3F6FC',outline='#DCE4F0',width=2)
        d.rounded_rectangle((100,y+40,162,y+102),radius=15,fill=PURPLE)
        text(im,f'{beat+1:02}',(112,y+54),27,55,'white')
        fs=43
        while len(wrap(label,fs,1530))*math.ceil(fs*1.25)>118:fs-=1
        text(im,label,(196,y+36),fs,1530)
    if not s['flow']:
        text(im,'Sumber: teks projek terdahulu • rujukan seksyen dalam storyboard',(80,815),24,1700,'#526885')
    d.line((76,982,1810,982),fill='#DCE4F0',width=3)
    text(im,'DRAF VISUAL • MASA ANGGARAN • MENUNGGU WAV LUDO' if DRAFT else 'BARU • UiTM | Narasi sintetik: Google AI Studio — Ludo',(76,1014),23,1560,'#526885',1080)
    text(im,f'{index+1:02}/08',(1730,1014),23,100,BLUE,1080)
    return im

def frame(index,t,span):
    s=SCENES[index];n=len(s['visual_beats']);beat=min(n-1,int(t/span*n));local=t-span*beat/n
    im=slide(index,beat).copy();d=ImageDraw.Draw(im)
    # A short reveal, followed by an animated flow focus and continuous progress.
    reveal=min(1,local/.45)
    if reveal<1:
        cover=Image.new('RGB',(W,H),'white');cover.paste(im.crop((0,0,W,255)),(0,0));cover.paste(im.crop((0,970,W,H)),(0,970))
        im=Image.blend(cover,im,1-(1-reveal)**3);d=ImageDraw.Draw(im)
    flow=s['flow']
    if flow:
        cell=1680/len(flow);active=min(len(flow)-1,int((local/max(.01,span/n))*len(flow)))
        for j,label in enumerate(flow):
            x=80+j*cell;right=x+cell-30
            d.rounded_rectangle((x,780,right,898),radius=17,fill=PURPLE if j==active else '#EEF2F8')
            fs=29
            while len(wrap(label,fs,cell-64))>2:fs-=1
            lines=wrap(label,fs,cell-64)
            for k,line in enumerate(lines):
                xx=x+(cell-30-font(fs).getlength(line))/2
                d.text((xx,815+k*34),line,font=font(fs),fill='white' if j==active else BLUE,anchor='lt')
            if j<len(flow)-1:
                xx=right+9;d.line((xx,839,xx+20,839),fill=PURPLE,width=3);d.polygon([(xx+20,839),(xx+11,832),(xx+11,846)],fill=PURPLE)
    if not DRAFT:
        for c in captions(index):
            if c['start']+.25<=t<c['end']+.25:
                fs=32
                while len(wrap(c['text'],fs,1660))>2 and fs>24:fs-=1
                lines=wrap(c['text'],fs,1660)
                if len(lines)>2:raise ValueError('Pecahkan cue kapsyen yang terlalu panjang.')
                d.rounded_rectangle((76,902,1805,974),radius=10,fill='#F3F6FC')
                for k,line in enumerate(lines):
                    x=(W-font(fs).getlength(line))/2
                    d.text((x,906+k*34),line,font=font(fs),fill=BLUE,anchor='lt')
                break
    d.line((76,982,76+1734*min(1,t/span),982),fill=PURPLE,width=5)
    return im

@lru_cache(None)
def captions(index):
    return json.loads((ROOT/'audio'/f"{SCENES[index]['id']}.cues.json").read_text())

def encode(index,seconds,target):
    proc=subprocess.Popen(['ffmpeg','-v','error','-nostdin','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-an','-c:v','libx264','-threads','2','-crf','23','-preset','veryfast','-pix_fmt','yuv420p','-movflags','+faststart',str(target)],stdin=subprocess.PIPE)
    try:
        for k in range(round(seconds*FPS)):proc.stdin.write(frame(index,k/FPS,seconds).tobytes())
    finally:proc.stdin.close()
    if proc.wait():raise RuntimeError('FFmpeg render failed')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--draft',action='store_true');args=parser.parse_args()
    out=ROOT/'outputs';out.mkdir(exist_ok=True);qa=ROOT/'qa';qa.mkdir(exist_ok=True)
    sheet=Image.new('RGB',(960,4*270),'white')
    for i,s in enumerate(SCENES):
        for j in range(len(s['visual_beats'])):
            frame(i,(j+.5)*s['duration_target']/len(s['visual_beats']),s['duration_target']).save(out/f"{s['id']}_visual_{j+1:02}.png")
        image=frame(i,s['duration_target']*.45,s['duration_target']);sheet.paste(image.resize((480,270)),((i%2)*480,(i//2)*270))
    sheet.save(out/'Pratonton_8_Babak.png')
    report={'native_resolution':[W,H],'fps':FPS,'scenes':len(SCENES),'visual_beats':sum(len(s['visual_beats']) for s in SCENES),'text_bounds':'passed','text_items_checked':len(AUDIT),'timing':'estimated, not aligned to real WAV','ludo_audio':'missing','final_video':'not generated','final_qa':'blocked by missing Ludo audio'}
    if args.draft:
        cache=ROOT/'rendered';cache.mkdir(exist_ok=True);parts=[]
        for i,s in enumerate(SCENES):
            target=cache/f"{s['id']}-visual-draft.mp4";encode(i,s['duration_target'],target);parts.append(target)
            print('Rendered',s['id'],s['duration_target'],'seconds (silent draft)',flush=True)
        listing=cache/'draft-concat.txt';listing.write_text(''.join(f"file '{p.as_posix()}'\n" for p in parts))
        target=out/'DRAF_330s_FHD_TANPA_AUDIO.mp4'
        subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(target)],check=True)
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(target)]))
        video=probe['streams'][0]
        assert video['codec_name']=='h264' and video['width']==W and video['height']==H and video['r_frame_rate']=='30/1'
        assert len(probe['streams'])==1 and abs(float(probe['format']['duration'])-330)<.05
        subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
        report.update(draft_codec='h264',draft_seconds=float(probe['format']['duration']),draft_decode='passed',audio_streams=0)
    (qa/'visual-draft-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)
if __name__=='__main__':main()
