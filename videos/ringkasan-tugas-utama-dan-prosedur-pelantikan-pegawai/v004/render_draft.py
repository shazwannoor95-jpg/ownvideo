"""Native FHD editorial preview. Contains original music, no generated speech.
All timings are estimated until verified Google AI Studio Ludo recordings exist.
"""
from pathlib import Path
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
import argparse, json, math, subprocess
from PIL import Image, ImageDraw, ImageFont
R=Path(__file__).resolve().parent
W,H,FPS=1920,1080,30
NAVY='#102B53'; PURPLE='#792A87'; GOLD='#EAB33E'; INK='#273B57'; MUTED='#63738B'; PALE='#F3F5FA'; LINE='#DDE3ED'
SCENES=json.loads((R/'storyboard.json').read_text())['scenes']
AUDIT=[]
@lru_cache(None)
def font(size,bold=False):
 f=ImageFont.truetype(str(R/'local_resources/Outfit[wght].ttf'),size)
 f.set_variation_by_axes([650 if bold else 430]); return f

def lines(txt,size,width,bold=False):
 out=[]
 for para in txt.split('\n'):
  row=''
  for word in para.split():
   test=(row+' '+word).strip()
   if row and font(size,bold).getlength(test)>width:out.append(row);row=word
   else:row=test
  out.append(row)
 return out

def text(im,txt,x,y,size=30,width=1500,color=INK,bold=False,maxheight=None):
 ls=lines(txt,size,width,bold);step=math.ceil(size*1.22)
 if maxheight is not None:
  assert len(ls)*step<=maxheight,(txt,size,len(ls)*step,maxheight)
 box=(x,y,x+max((font(size,bold).getlength(l) for l in ls),default=0),y+step*len(ls))
 assert box[0]>=0 and box[1]>=0 and box[2]<=W and box[3]<=H,(txt,box)
 d=ImageDraw.Draw(im)
 for i,l in enumerate(ls):d.text((x,y+i*step),l,font=font(size,bold),fill=color,anchor='lt')
 AUDIT.append({'text':txt,'bounds':box,'size':size})
 return y+len(ls)*step

def fit(im,txt,x,y,size,width,maxheight,color=INK,bold=False,minsize=24):
 while len(lines(txt,size,width,bold))*math.ceil(size*1.22)>maxheight and size>minsize:size-=1
 return text(im,txt,x,y,size,width,color,bold,maxheight)

@lru_cache(None)
def logo():
 a=Image.open(R/'assets/brand/LogoUiTM.png').convert('RGBA');a.thumbnail((220,105));return a

def document(d,x,y,scale=1,color=PURPLE):
 s=scale
 d.rounded_rectangle((x,y,x+170*s,y+210*s),radius=16*s,outline=color,width=max(2,int(6*s)),fill='white')
 for k,l in enumerate([110,90,110,70]):d.line((x+28*s,y+(55+k*32)*s,x+(28+l)*s,y+(55+k*32)*s),fill=color,width=max(2,int(5*s)))

def base(idx):
 im=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(im)
 d.rectangle((0,0,16,H),fill=PURPLE)
 d.ellipse((1590,120,2200,730),fill='#FAF7FB')
 d.ellipse((1800,740,2200,1140),fill='#FBF8F1')
 im.paste(logo(),(1610,30),logo())
 text(im,'BAHAGIAN ARKIB UNIVERSITI',(86,50)[0],50,23,1450,PURPLE,True)
 text(im,'UNIVERSITI TEKNOLOGI MARA',86,86,20,1400,MUTED)
 d.line((86,1000,1834,1000),fill=LINE,width=3)
 text(im,'PRATONTON • NARASI LUDO BELUM DIMASUKKAN',86,1027,21,1300,MUTED)
 text(im,f'SLAID {idx+1:02} / 09',1645,1027,21,200,NAVY,True)
 return im

def badge(im,label,x,y,w=200):
 d=ImageDraw.Draw(im);d.rounded_rectangle((x,y,x+w,y+46),radius=23,fill=PURPLE)
 text(im,label,x+20,y+12,20,w-36,'white',True,maxheight=28)

def role(idx,beat,active,flow_active):
 s=SCENES[idx];b=s['beats'][beat];im=base(idx);d=ImageDraw.Draw(im)
 badge(im,'PELANTIKAN '+s['number'],86,150,220)
 fit(im,s['title']+(f"  ({s['short']})" if s.get('short') else ''),86,217,58,1730,98,NAVY,True)
 text(im,s['reference'],88,300,24,1690,MUTED)
 # Static credential panel.
 d.rounded_rectangle((86,356,582,834),radius=26,fill=NAVY)
 y=387
 for label,val in [('PEGAWAI YANG LAYAK',s['eligible']),('PIHAK PELANTIK / KUASA',s['appoint']),('BORANG',s['form'])]:
  text(im,label,116,y,19,430,'#BFCDE1',True);y+=33
  end=fit(im,val,116,y,31,428,86,'white',True)
  y=end+24
  if label!='BORANG':d.line((116,y-9,550,y-9),fill='#3A5272',width=1)
 # Dynamic teaching panel.
 text(im,f"{beat+1:02} / 03",632,363,23,200,PURPLE,True)
 fit(im,b['title'],632,404,40,1185,90,NAVY,True)
 for j,item in enumerate(b['items']):
  top=513+j*103
  d.rounded_rectangle((630,top,1834,top+88),radius=18,fill='#F5EEF7' if j==active else PALE,outline=PURPLE if j==active else LINE,width=2)
  d.ellipse((652,top+25,690,top+63),fill=PURPLE if j==active else '#D6DEEB')
  text(im,str(j+1),665,top+34,19,25,'white' if j==active else NAVY,True)
  fit(im,item,713,top+18,30,1090,65,INK,j==active)
 # Notes and agency, then flow row.
 fit(im,s['note'],88,857,25,1730,60,MUTED)
 flow=s['flow']
 if flow:
  n=len(flow);cw=1748/n
  for j,label in enumerate(flow):
   x=86+j*cw;right=x+cw-35
   d.rounded_rectangle((x,926,right,979),radius=14,fill=PURPLE if j==flow_active else '#EEF1F7')
   fs=24
   while font(fs,True).getlength(label)>cw-65:fs-=1
   xx=x+(cw-35-font(fs,True).getlength(label))/2
   text(im,label,xx,943,fs,cw-45,'white' if j==flow_active else NAVY,True)
   if j<n-1:
    d.line((right+8,952,right+25,952),fill=PURPLE,width=2)
    d.polygon([(right+25,952),(right+18,946),(right+18,958)],fill=PURPLE)
 else:
  text(im,'AGENSI TERLIBAT  /  '+s['agency'],88,942,25,1700,PURPLE,True)
 return im

def intro(active):
 im=base(0);d=ImageDraw.Draw(im)
 badge(im,'PANDUAN RINGKAS',86,171,240)
 text(im,'Pelantikan\npegawai',86,266,108,1060,NAVY,True)
 text(im,'Tugas utama dan prosedur\ndi Universiti Teknologi MARA',92,554,41,1060,MUTED)
 # Restrained original vector illustration.
 d.rounded_rectangle((1320,240,1800,743),radius=42,fill='#F1E8F5')
 d.ellipse((1400,285,1728,613),fill='white')
 document(d,1436,324,1.12)
 badge(im,'06 PERANAN',1400,652,295)
 for j,label in enumerate(SCENES[0]['beats'][0]['items']):
  x=86+j*588
  d.rounded_rectangle((x,806,x+557,938),radius=22,fill=PURPLE if j==active else PALE)
  text(im,f'{j+1:02}',x+24,825,26,70,GOLD,True)
  fit(im,label,x+24,866,28,510,68,'white' if j==active else NAVY,True)
 return im

def overview(active):
 im=base(1);d=ImageDraw.Draw(im)
 badge(im,'GAMBARAN KESELURUHAN',86,151,355)
 text(im,'Enam pelantikan,',86,227,66,1710,NAVY,True)
 text(im,'tiga bidang utama',86,311,66,1710,NAVY,True)
 pairs=[('01 / 02','PENGELASAN\nRAHSIA RASMI'),('03 / 04','PENGURUSAN\nREKOD'),('05 / 06','PENDAFTARAN\nRAHSIA')]
 for j,(number,title) in enumerate(pairs):
  x=86+j*588;hot=j==active
  d.rounded_rectangle((x,457,x+556,849),radius=26,fill=NAVY if hot else PALE,outline=NAVY if hot else LINE,width=2)
  text(im,number,x+30,491,36,470,GOLD if hot else PURPLE,True)
  text(im,title,x+30,555,34,470,'white' if hot else NAVY,True)
  for k,item in enumerate(SCENES[1]['beats'][j]['items']):
   fit(im,item,x+30,675+k*72,27,475,70,'#D4DFEF' if hot else MUTED)
 text(im,'Kelayakan  •  Pihak pelantik  •  Tugas  •  Borang  •  Aliran urusan',88,915,29,1740,MUTED)
 return im

def summary(active):
 im=base(8);d=ImageDraw.Draw(im)
 badge(im,'RINGKASAN & PENUTUP',86,151,330)
 text(im,'Peranan jelas, tindakan teratur.',86,226,62,1730,NAVY,True)
 rows=[('Pengelas Semula','Naib Canselor / Rektor','KPT, CGSO','KPKK 9(A)'),('Pegawai Pengelas','Ketua Jabatan / Bahagian / Unit','JPT, KPT, CGSO','Seksyen 2B + KPKK 9'),('PRJ','Gred 5 dan ke atas','ANM','SKL 8'),('PTRJ','Gred 1 dan ke atas*','ANM','SKL 8'),('Pendaftar Rahsia','Gred 1 dan ke atas yang berkenaan','CGSO','KPKK 22'),('Pendaftar Kecil Rahsia','Gred 1 dan ke atas yang berkenaan','CGSO','KPKK 22')]
 cols=[86,602,1190,1442];widths=[490,555,230,370]
 d.rounded_rectangle((86,352,1834,414),radius=14,fill=NAVY)
 for x,label,width in zip(cols,['PELANTIKAN','PEGAWAI / GRED','AGENSI','BORANG'],widths):text(im,label,x+18,374,21,width,'white',True)
 for i,row in enumerate(rows):
  y=424+i*72;hot=i==active
  d.rounded_rectangle((86,y,1834,y+63),radius=11,fill='#F0E7F4' if hot else ('#F5F7FB' if i%2==0 else 'white'))
  if hot:d.rounded_rectangle((86,y,94,y+63),radius=4,fill=PURPLE)
  for j,(x,label,width) in enumerate(zip(cols,row,widths)):
   fit(im,label,x+18,y+15,26,width-20,43,PURPLE if hot else INK,j==0,minsize=18)
 text(im,'*Gred PTRJ dan aliran dalaman yang belum disahkan perlu disemak oleh BARU',88,888,27,1720,MUTED)
 text(im,'sebelum edaran rasmi. Sumber slaid: draf untuk semakan dalaman.',88,927,27,1720,MUTED)
 return im

def make_frames():
 out=R/'outputs';out.mkdir(exist_ok=True);cache=R/'rendered';cache.mkdir(exist_ok=True)
 segments=[];t=0
 for idx,s in enumerate(SCENES):
  frames=[]
  if s['kind']=='intro':frames=[intro(i) for i in range(3)]
  elif s['kind']=='overview':frames=[overview(i) for i in range(3)]
  elif s['kind']=='summary':frames=[summary(i) for i in range(6)]
  else:
   for b,beat in enumerate(s['beats']):
    for a in range(len(beat['items'])):
     flow_index=min(len(s['flow'])-1,int((b+a/len(beat['items']))/3*len(s['flow']))) if s['flow'] else -1
     frames.append(role(idx,b,a,flow_index))
  # Integer frame boundaries ensure exact final duration.
  total=s['duration_target']*FPS
  for j,im in enumerate(frames):
   start=round(j*total/len(frames));end=round((j+1)*total/len(frames));dur=(end-start)/FPS
   file=cache/f'{s["id"]}_{j:02}.png';im.save(file)
   segments.append({'source':str(file),'target':str(cache/f'{s["id"]}_{j:02}.mp4'),'start_seconds':t,'duration':dur,'frames':end-start,'scene':s['id']});t+=dur
  frames[len(frames)//2].save(out/f'{s["id"]}_Pratonton.png')
 sheet=Image.new('RGB',(1440,810),'white')
 for i,s in enumerate(SCENES):
  im=Image.open(out/f'{s["id"]}_Pratonton.png');im.thumbnail((480,270));sheet.paste(im,((i%3)*480,(i//3)*270))
 sheet.save(out/'Pratonton_9_Babak.jpg',quality=93)
 (R/'qa/layout-check.json').write_text(json.dumps({'status':'passed','checked_text_elements':len(AUDIT),'bounds_checked':True,'resolution':[W,H],'text':AUDIT},ensure_ascii=False,indent=2))
 (R/'qa/estimated-segments.json').write_text(json.dumps(segments,indent=2))
 return segments

def encode(seg):
 duration=seg['duration'];start=seg['start_seconds'];fade=min(.22,duration/8)
 # The gold marker moves over the progress rule on every output frame.
 graph=f"[0:v]format=yuv420p,fade=t=in:st=0:d={fade}:color=white[page];[page][1:v]overlay=x='86+1736*({start}+t)/360':y=996:shortest=1,format=yuv420p[v]"
 subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-loop','1','-framerate','30','-i',seg['source'],'-f','lavfi','-i','color=c=0xEAB33E:s=12x9:r=30','-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-frames:v',str(seg['frames']),'-an','-c:v','libx264','-threads','2','-crf','22','-preset','veryfast','-pix_fmt','yuv420p',seg['target']],check=True)
 return seg['target']

def assemble(segments):
 with ThreadPoolExecutor(max_workers=2) as pool:
  for i,result in enumerate(pool.map(encode,segments),1):
   print(f'Render {i}/{len(segments)}: {Path(result).name}',flush=True)
 listing=R/'rendered/concat.txt';listing.write_text(''.join("file '"+s['target']+"'\n" for s in segments))
 target=R/'outputs/DRAF_6_MINIT_MUZIK_MENUNGGU_LUDO.mp4'
 subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-f','concat','-safe','0','-i',str(listing),'-i',str(R/'audio/muzik-korporat.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af','volume=0.65','-c:a','aac','-b:a','160k','-t','360','-movflags','+faststart','-metadata','title=Ringkasan Pelantikan Pegawai UiTM — Pratonton Menunggu Ludo',str(target)],check=True)
 print('DRAFT_SAVED',target,flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--encode',action='store_true');a=p.parse_args()
 segs=make_frames()
 print(json.dumps({'segments':len(segs),'seconds':sum(s['duration'] for s in segs),'words':sum(len(s['narration'].split()) for s in SCENES)}),flush=True)
 if a.encode:assemble(segs)
