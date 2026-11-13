"""Native Full HD visual production. Proof is silent and is NOT the final video."""
from pathlib import Path
from functools import lru_cache
import json,math,subprocess,argparse
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
W,H=1920,1080
BLUE='#042E6F';PURPLE='#92278F';GOLD='#FEBE10'
@lru_cache(None)
def font(size):return ImageFont.truetype(str(ROOT/'local_resources/Outfit[wght].ttf'),size)
def wrap(text,size,width):
 lines=[];line=''
 for word in text.split():
  c=(line+' '+word).strip()
  if line and font(size).getlength(c)>width:lines.append(line);line=word
  else:line=c
 if line:lines.append(line)
 return lines
def text(draw,value,xy,size=36,width=1550,fill=BLUE):
 for i,line in enumerate(wrap(value,size,width)):draw.text((xy[0],xy[1]+i*int(size*1.22)),line,font=font(size),fill=fill)
def frame(scene,index,t,span=8):
 im=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(im)
 d.rectangle((0,0,20,H),fill=PURPLE);d.polygon([(1700,240),(1920,180),(1920,1080),(1810,1080)],fill='#F7F2F8')
 logo=Image.open(ROOT/'assets/brand/LogoUiTM.png').convert('RGBA');logo.thumbnail((270,138));im.paste(logo,(1590,34),logo)
 text(d,'BARU • UNIVERSITI TEKNOLOGI MARA',(76,40),24,1400,PURPLE)
 text(d,scene['chapter'],(76,105),47,1450)
 text(d,scene['title'],(76,175),29,1450,'#526885')
 n=len(scene['bullets']);height=min(126,int(660/n)-16);bounds=[]
 for j,b in enumerate(scene['bullets']):
  progress=max(0,min(1,(t-.2-j*.20)/.5));x=round(88+(1-progress)*45);y=282+j*(height+14)
  if progress<=0:continue
  d.rounded_rectangle((x,y,1800,y+height),radius=18,fill='#F3F6FC',outline='#DCE4F0',width=2)
  d.rounded_rectangle((x+18,y+21,x+68,y+71),radius=10,fill=PURPLE)
  text(d,f'{j+1:02}',(x+26,y+26),25,50,'white')
  fs=35
  while len(wrap(b,fs,1570))*fs*1.22>height-22:fs-=1
  if fs<23:raise ValueError('Text too long: '+b)
  lines=wrap(b,fs,1570);yy=y+(height-len(lines)*fs*1.22)/2
  text(d,b,(x+94,yy),fs,1570)
  bounds.append((x+94,yy,x+94+1570,yy+len(lines)*fs*1.22))
 d.line((76,988,1810,988),fill='#DCE4F0',width=3);d.line((76,988,76+int(1734*min(1,t/span)),988),fill=PURPLE,width=5)
 text(d,'DRAF VISUAL • Menunggu WAV Ludo • BUKAN VIDEO AKHIR',(76,1015),22,1560,'#526885')
 text(d,f'{index+1:02}/08',(1735,1015),22,100)
 assert all(x>=0 and y>=0 and xx<=W and yy<980 for x,y,xx,yy in bounds)
 return im

def main():
 a=argparse.ArgumentParser();a.add_argument('--proof',action='store_true');args=a.parse_args()
 scenes=json.loads((ROOT/'storyboard.json').read_text())['scenes'];out=ROOT/'outputs';out.mkdir(exist_ok=True)
 sheet=Image.new('RGB',(960,4*292),'white')
 for i,s in enumerate(scenes):
  for t in [0,.4,.8,1.6,3,5,7.9]:frame(s,i,t)
  image=frame(s,i,7.5);image.save(out/f"Pratonton_{s['id']}.png")
  sheet.paste(image.resize((480,270)),((i%2)*480,(i//2)*292))
 sheet.save(out/'Pratonton_8_Babak.png')
 (ROOT/'qa/visual-draft-check.json').write_text(json.dumps({'status':'passed','native_resolution':[W,H],'scenes':len(scenes),'samples_per_scene':7,'text_bounds':'passed','audio':'not generated','final_video':'not generated'},indent=2))
 if args.proof:
  target=out/'DRAF_Animasi_TANPA_AUDIO.mp4'
  proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-an','-c:v','libx264','-threads','2','-crf','23','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(target)],stdin=subprocess.PIPE)
  try:
   for k in range(240):proc.stdin.write(frame(scenes[2],2,k/30).tobytes())
  finally:proc.stdin.close()
  if proc.wait():raise RuntimeError('Proof render failed')
  subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
 print('PASS: 8 native Full HD visual previews; no final video or Ludo claimed.')
if __name__=='__main__':main()
