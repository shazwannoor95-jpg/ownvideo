import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import video

class VersionTests(unittest.TestCase):
    def test_title_versions_are_independent_and_remote_aware(self):
        self.assertEqual(video.slugify('Pelantikan Pegawai — UiTM!'),'pelantikan-pegawai-uitm')
        refs='abc\trefs/heads/video/tajuk/v003\ndef\trefs/tags/tajuk-v007\nabc\trefs/heads/video/lain/v999\n'
        self.assertEqual(video.next_version('tajuk',refs),'v008')
        self.assertEqual(video.next_version('baharu',refs),'v001')
        with self.assertRaises(ValueError):video.slugify('!!!')

    def test_source_words_are_kept_and_cards_bounded(self):
        text='# Peranan\n'+('Tugas pengurusan rekod jabatan. '*70)
        story=video.create_story('Video',text)
        spoken=' '.join(s['narration'] for s in story['scenes'])
        self.assertEqual(' '.join(spoken.split()),' '.join(text.split('\n',1)[1].split()))
        self.assertTrue(all(len(s['bullets'])<=3 for s in story['scenes']))

class LifecycleTests(unittest.TestCase):
    def test_real_render_publish_and_next_version_from_clean_checkout(self):
        # No GitHub or original workspace path is needed by the generated video.
        with tempfile.TemporaryDirectory(prefix='ownvideo-test-') as tmp:
            root=Path(tmp);repo=root/'repo';repo.mkdir();remote=root/'remote.git'
            def git(*args,cwd=repo):
                return subprocess.run(['git',*args],cwd=cwd,check=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
            git('init','--bare',remote,cwd=root)
            git('init','-b','main');git('config','user.name','Workflow Test');git('config','user.email','test@example.invalid')
            shutil.copytree(ROOT/'tools',repo/'tools',ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copy2(ROOT/'.gitignore',repo/'.gitignore')
            git('add','.');git('commit','-m','tools');git('remote','add','origin',remote);git('push','-u','origin','main')
            source=root/'bahan.md';source.write_text('# Ujian\nIni ujian suara Melayu. Rekod disimpan dengan teratur.')
            old=video.REPO;video.REPO=repo
            try:
                p=video.new('Ujian Video',source)
                self.assertEqual(git('branch','--show-current').strip(),'video/ujian-video/v001')
                video.render(p,1)
                info=json.loads((p/'project.json').read_text())
                self.assertEqual(info['status'],'RENDERED')
                self.assertTrue((p/info['final_video']).is_file())
                self.assertTrue(json.loads((p/'qa/final-technical-report.json').read_text())['technical_checks_passed'])
                video.publish(p)
                self.assertIn('refs/tags/ujian-video-v001',git('ls-remote','origin'))
                p2=video.new('Ujian Video',source)
                self.assertEqual(p2.name,'v002')
                self.assertEqual(git('branch','--show-current').strip(),'video/ujian-video/v002')
            finally:video.REPO=old

if __name__=='__main__':unittest.main()
