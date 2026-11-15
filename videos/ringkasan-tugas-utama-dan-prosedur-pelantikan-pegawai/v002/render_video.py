"""Compatibility entry for ./video render; native 1920x1080 output."""
import argparse
from production import render
import render_fhd
p=argparse.ArgumentParser();p.add_argument('--frames',action='store_true');p.add_argument('--all',action='store_true');p.add_argument('--workers',type=int,default=2);a=p.parse_args()
if a.frames:
    for i,s in enumerate(render_fhd.SCENES):
        render_fhd.frame(i,s.get('duration',s['duration_target'])*.5,s.get('duration',s['duration_target'])).save(render_fhd.ROOT/'outputs'/f"{s['id']}_preview.png")
if a.all:render()
