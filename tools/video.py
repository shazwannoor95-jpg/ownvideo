#!/usr/bin/env python3
"""Create, render and publish independent video branches named from each title."""
import argparse
import datetime
import hashlib
import json
import re
import shutil
import subprocess
import sys
import textwrap
import unicodedata
from pathlib import Path

REPO=Path(__file__).resolve().parents[1]

def run(args,cwd=None,capture=False):
    return subprocess.run([str(a) for a in args],cwd=cwd or REPO,check=True,text=True,
                          stdout=subprocess.PIPE if capture else None).stdout

def git(*args,capture=False):return run(['git',*args],capture=capture)

def slugify(title):
    name=unicodedata.normalize('NFKD',title).encode('ascii','ignore').decode().lower()
    name=re.sub('[^a-z0-9]+','-',name).strip('-')[:90].rstrip('-')
    if not name:raise ValueError('Tajuk mesti mengandungi sekurang-kurangnya satu huruf Latin atau nombor.')
    return name

def next_version(slug,refs):
    pattern=rf'(?:refs/heads/video/{re.escape(slug)}/v|refs/tags/{re.escape(slug)}-v)(\d+)(?:\s|$)'
    values=[int(n) for n in re.findall(pattern,refs)]
    for p in (REPO/'videos'/slug).glob('v[0-9]*'):
        if re.fullmatch(r'v\d+',p.name):values.append(int(p.name[1:]))
    return 'v'+str(max(values,default=0)+1).zfill(3)

def create_story(title,text):
    scenes=[];heading=title;items=[]
    def flush():
        nonlocal items
        if items:
            scenes.append({'id':f's{len(scenes)+1:02}','title':heading,'eyebrow':title,
                'layout':'source_cards','role':0,'bullets':items,'narration':' '.join(items),
                'source_refs':[{'source':'user_text','section':heading}]})
            items=[]
    for line in text.splitlines():
        line=line.strip()
        if not line or line=='---':continue
        if line.startswith('#'):
            flush();heading=line.lstrip('#').strip();continue
        line=re.sub(r'^[-*]\s+|^\d+[.)]\s+','',line).replace('**','').strip()
        # Split long paragraphs so source text fits on a 720p card without dropping words.
        chunks=textwrap.wrap(line,width=330,break_long_words=False,break_on_hyphens=False)
        for chunk in chunks:
            if items and (len(items)==3 or sum(map(len,items))+len(chunk)>600):flush()
            items.append(chunk)
    flush()
    if not scenes:raise ValueError('Sumber teks kosong.')
    return {'title':title,'language':'ms-MY','fps':30,'sources':[{'id':'user_text',
        'title':'Teks dibekalkan pengguna','path':'source/teks-pengguna.md'}],
        'pronunciation':{'UiTM':'yu ai ti em','CGSO':'si ji es o','PTj':'pusat tanggungjawab'},'scenes':scenes}

def new(title,source):
    title=title.strip()
    if not title:raise ValueError('Tajuk kosong.')
    text=Path(source).read_text(encoding='utf-8-sig')
    story=create_story(title,text)
    if git('status','--porcelain',capture=True).strip():raise ValueError('Simpan atau commit perubahan kerja sebelum mencipta branch video.')
    slug=slugify(title)
    refs=git('ls-remote','origin',capture=True)+'\n'+git('show-ref',capture=True)
    version=next_version(slug,refs);branch=f'video/{slug}/{version}'
    git('fetch','origin','main')
    git('switch','-c',branch,'origin/main')
    dest=REPO/'videos'/slug/version
    shutil.copytree(REPO/'tools/template',dest)
    for name in ['source','audio','qa','rendered','outputs']:(dest/name).mkdir(exist_ok=True)
    (dest/'source/teks-pengguna.md').write_text(text)
    (dest/'storyboard.json').write_text(json.dumps(story,ensure_ascii=False,indent=2)+'\n')
    info={'title':title,'slug':slug,'version':version,'branch':branch,'tag':f'{slug}-{version}',
          'status':'DRAFT','voiceover':{'provider':'Google AI Studio','voice':'Ludo'},
          'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (dest/'project.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
    print('Branch:',branch,'\nProjek:',dest.relative_to(REPO),'\nSeterusnya: ./video render',dest.relative_to(REPO))
    return dest

def project(path):
    p=Path(path)
    if not p.is_absolute():p=REPO/p
    p=p.resolve()
    if not p.is_relative_to(REPO/'videos'):raise ValueError('Folder projek mesti berada dalam videos/.')
    info=json.loads((p/'project.json').read_text())
    return p,info

def captions(p):
    story=json.loads((p/'storyboard.json').read_text());timings=json.loads((p/'timeline.json').read_text())
    out=p/'outputs';out.mkdir(exist_ok=True);rows=[];script=[]
    def stamp(t):
        v=round(t*1000);h,v=divmod(v,3600000);m,v=divmod(v,60000);s,ms=divmod(v,1000)
        return f'{h:02}:{m:02}:{s:02},{ms:03}'
    for scene,timing in zip(story['scenes'],timings['scenes'],strict=True):
        script.append(scene['eyebrow']+' — '+scene['title']+'\n'+scene['narration']+'\n')
        for cue in json.loads((p/'audio'/f"{scene['id']}.cues.json").read_text()):
            a=timing['start_seconds']+.25+cue['start'];b=timing['start_seconds']+.25+cue['end']
            if b>timing['end_seconds']+.02:raise ValueError('Kapsyen melebihi masa babak.')
            rows.append(f'{len(rows)+1}\n{stamp(a)} --> {stamp(b)}\n'+'\n'.join(textwrap.wrap(cue['text'],72))+'\n')
    (out/'Kapsyen_BM.srt').write_text('\n'.join(rows))
    (out/'Skrip_Narasi_BM.txt').write_text('\n'.join(script))
    return out/'Kapsyen_BM.srt'

def package(p,info):
    srt=captions(p);base=p/'outputs'/f"{info['slug']}-{info['version']}.mp4"
    final=base.with_name(base.stem+'-kapsyen.mp4')
    story=json.loads((p/'storyboard.json').read_text())
    timeline=json.loads((p/'timeline.json').read_text())
    chapters=[]
    for scene,timing in zip(story['scenes'],timeline['scenes'],strict=True):
        label=scene.get('eyebrow') or scene['title']
        if not chapters or chapters[-1]['label']!=label:
            chapters.append({'label':label,'start':timing['start_seconds'],'end':timing['end_seconds']})
        else:chapters[-1]['end']=timing['end_seconds']
    metadata=[';FFMETADATA1']
    for chapter in chapters:
        label=chapter['label'].replace('\\','\\\\').replace('=','\\=').replace(';','\\;').replace('#','\\#').replace('\n',' ')
        metadata+=['[CHAPTER]','TIMEBASE=1/1000',f"START={round(chapter['start']*1000)}",f"END={round(chapter['end']*1000)}",'title='+label]
    chapterfile=p/'qa/chapters.ffmeta';chapterfile.parent.mkdir(exist_ok=True)
    chapterfile.write_text('\n'.join(metadata)+'\n')
    run(['ffmpeg','-v','error','-y','-i',base,'-i',srt,'-i',chapterfile,'-map_chapters','2','-map','0:v:0','-map','0:a:0','-map','1:0',
         '-c','copy','-c:s','mov_text','-metadata:s:s:0','language=msa','-movie_timescale','1000','-movflags','+faststart+disable_chpl',final])
    run(['ffmpeg','-v','error','-i',final,'-map','0:v:0','-map','0:a:0','-f','null','-'])
    report=json.loads((p/'qa/final-technical-report.json').read_text())
    if not report['technical_checks_passed']:raise ValueError('Semakan teknikal gagal.')
    info.update(status='RENDERED',final_video=final.relative_to(p).as_posix(),
        final_sha256=hashlib.sha256(final.read_bytes()).hexdigest())
    (p/'project.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
    print('SIAP:',final.relative_to(REPO))

def render(path,workers,resynthesize=False,frames_only=False):
    p,info=project(path)
    if not 1<=workers<=4:raise ValueError('Pilih 1 hingga 4 worker.')
    if resynthesize:
        raise ValueError('Jana semula narasi melalui Google AI Studio dengan suara Ludo, gantikan WAV dan cues yang telah disemak, kemudian render tanpa --resynthesize. Tiada fallback suara automatik.')
    missing=[f"audio/{s['id']}{suffix}" for s in json.loads((p/'storyboard.json').read_text())['scenes']
             for suffix in ['.wav','.cues.json'] if not (p/'audio'/f"{s['id']}{suffix}").is_file()]
    if missing:
        raise ValueError('WAV Ludo dan cap masa kapsyen diperlukan daripada Google AI Studio: '+', '.join(missing))
    run([sys.executable,'produce.py','--prepare'],cwd=p)
    run([sys.executable,'render_video.py','--frames'],cwd=p)
    if frames_only:return
    run([sys.executable,'render_video.py','--all','--workers',workers],cwd=p)
    run([sys.executable,'produce.py','--assemble'],cwd=p)
    package(p,info)

def publish(path):
    p,info=project(path);branch=git('branch','--show-current',capture=True).strip()
    if branch!=info['branch']:raise ValueError('Checkout branch projek terlebih dahulu: '+info['branch'])
    if info.get('status')!='RENDERED':raise ValueError('Render dan sahkan video sebelum publish.')
    final=p/info['final_video']
    if hashlib.sha256(final.read_bytes()).hexdigest()!=info['final_sha256']:raise ValueError('Hash video telah berubah.')
    if git('diff','--cached','--name-only',capture=True).strip():raise ValueError('Index Git mesti kosong sebelum publish.')
    rel=p.relative_to(REPO).as_posix()
    for file in p.rglob('*'):
        if file.is_file() and file.stat().st_size > 100*1024*1024:
            ignored=subprocess.run(['git','check-ignore','-q',str(file.relative_to(REPO))],cwd=REPO).returncode==0
            if not ignored:raise ValueError('Fail melebihi had GitHub 100 MiB: '+str(file))
    git('add','--',rel)
    staged=git('diff','--cached','--name-only',capture=True).splitlines()
    if any(not s.startswith(rel+'/') for s in staged):raise ValueError('Fail di luar projek ditemui dalam index.')
    if staged:git('commit','-m',f"video: {info['title']} ({info['version']})")
    head=git('rev-parse','HEAD',capture=True).strip()
    existing=run(['git','tag','--list',info['tag']],capture=True).strip()
    if existing:
        if git('rev-list','-n','1',info['tag'],capture=True).strip()!=head:raise ValueError('Tag versi sudah digunakan untuk commit lain.')
    else:git('tag','-a',info['tag'],'-m',f"{info['title']} — {info['version']}")
    git('push','--atomic','origin',f'HEAD:refs/heads/{branch}',f'refs/tags/{info["tag"]}')
    refs=git('ls-remote','origin',f'refs/heads/{branch}',f'refs/tags/{info["tag"]}^{{}}',capture=True)
    if not all(head+'\t'+ref in refs for ref in [f'refs/heads/{branch}',f'refs/tags/{info["tag"]}^{{}}']):raise ValueError('Pengesahan remote tidak sepadan.')
    print('PUBLISHED:',branch,info['tag'])

def main():
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='action',required=True)
    a=sub.add_parser('new');a.add_argument('title');a.add_argument('--source',required=True)
    a=sub.add_parser('render');a.add_argument('project');a.add_argument('--workers',type=int,default=2);a.add_argument('--resynthesize',action='store_true');a.add_argument('--frames-only',action='store_true')
    a=sub.add_parser('package');a.add_argument('project')
    a=sub.add_parser('publish');a.add_argument('project')
    args=ap.parse_args()
    if args.action=='new':new(args.title,args.source)
    elif args.action=='render':render(args.project,args.workers,args.resynthesize,args.frames_only)
    elif args.action=='package':package(*project(args.project))
    else:publish(args.project)
if __name__=='__main__':
    try:main()
    except (ValueError,subprocess.CalledProcessError) as exc:
        print('GAGAL:',exc,file=sys.stderr);sys.exit(1)
