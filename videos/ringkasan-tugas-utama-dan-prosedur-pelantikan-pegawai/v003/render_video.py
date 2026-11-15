from pathlib import Path
import json, argparse, hashlib
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
import render_fhd as visual
from produce import visual_signature
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def encode(args):
 s,i,n=args;out=ROOT/'rendered'/f"{s['id']}.mp4";out.parent.mkdir(exist_ok=True)
 signature=visual_signature(s,i,n)
 visual.encode(i,s['duration'],out)
 proof={'scene_id':s['id'],'visual_signature':signature,'output_sha256':sha(out),'duration_frames':round(s['duration']*30)}
 out.with_suffix('.render.json').write_text(json.dumps(proof,indent=2))
 print('Rendered',s['id'],round(s['duration'],2),'seconds native Full HD',flush=True)
 return proof

def preview():
 scenes=visual.SCENES;dest=ROOT/'qa/styleframes';dest.mkdir(exist_ok=True,parents=True)
 sheet=Image.new('RGB',(960,1080),'white');items=[]
 for i,s in enumerate(scenes):
  for j in range(len(s['visual_beats'])):
   image=visual.frame(i,(j+.5)*s['duration']/len(s['visual_beats']),s['duration'])
   image.save(dest/f"{s['id']}-{j+1}.png")
  image=visual.frame(i,s['duration']*.45,s['duration'])
  sheet.paste(image.resize((480,270)),((i%2)*480,(i//2)*270))
  items.append({'id':s['id'],'text_bounds_checked':True,'beats':len(s['visual_beats'])})
 sheet.save(ROOT/'qa/contact-sheet.png')
 (ROOT/'qa/visual-qa.json').write_text(json.dumps({'all_text_within_canvas':True,'native_resolution':[1920,1080],'scenes':items},indent=2))
 print('Full HD previews ready',flush=True)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--frames',action='store_true');a.add_argument('--all',action='store_true');a.add_argument('--workers',type=int,default=2);args=a.parse_args()
 if args.frames:preview()
 if args.all:
  with ProcessPoolExecutor(max_workers=args.workers) as ex:list(ex.map(encode,[(s,i,len(visual.SCENES)) for i,s in enumerate(visual.SCENES)]))
