"""Run only after real Ludo inputs and review; export the requested filenames."""
from pathlib import Path
import json,shutil,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[2]/'tools'))
import video
video.render(ROOT,2)
info=json.loads((ROOT/'project.json').read_text())
shutil.copyfile(ROOT/info['final_video'],ROOT/'outputs/Video_Pelantikan_Pegawai_UiTM_Final.mp4')
shutil.copyfile(ROOT/'outputs/Kapsyen_BM.srt',ROOT/'outputs/Video_Pelantikan_Pegawai_UiTM.srt')
print('Ready for human final review and ./video publish:',ROOT)
