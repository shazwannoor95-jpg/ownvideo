const {app,BrowserWindow,session,shell,ipcMain,dialog}=require('electron');
const path=require('node:path'),fs=require('node:fs'),{pathToFileURL}=require('node:url');
const {BrowserSession}=require('./ludo/browser-session.cjs');const {loadProject,generate}=require('./ludo/project.cjs');
const profile=process.env.OWNVIDEO_LUDO_PROFILE||path.join(__dirname,'../.cache/ludo-profile');
app.setPath('userData',path.resolve(profile));
let control,browser,selected,job;const dashboard=pathToFileURL(path.join(__dirname,'index.html')).href;
function bind(name,fn){ipcMain.handle('ludo:'+name,async e=>{
 if(e.sender!==control?.webContents||e.senderFrame?.url!==dashboard)throw Error('Pemanggil tidak dibenarkan.');
 try{return await fn();}catch(error){return {error:error.message};}
});}
app.whenReady().then(async()=>{
 if(process.argv.includes('--fixture-audit')||process.argv.includes('--live-audit')){await require('./tests/electron-audit.cjs').run({app,BrowserWindow,session,shell,live:process.argv.includes('--live-audit')});return;}
 if(!app.requestSingleInstanceLock()){app.quit();return;}
 browser=new BrowserSession({BrowserWindow,session,shell});
 const proxy=process.env.HTTPS_PROXY;
 if(proxy)await session.fromPartition('persist:ownvideo-ludo').setProxy({proxyRules:proxy});
 control=new BrowserWindow({width:1120,height:850,title:'ownvideo — Google AI Studio Ludo',webPreferences:{preload:path.join(__dirname,'preload.cjs'),contextIsolation:true,nodeIntegration:false,sandbox:true}});
 control.webContents.setWindowOpenHandler(()=>({action:'deny'}));control.webContents.on('will-navigate',e=>e.preventDefault());
 bind('choose',async()=>{if(job)throw Error('Penjanaan sedang berjalan.');const r=await dialog.showOpenDialog(control,{title:'Pilih storyboard.json',filters:[{name:'Storyboard JSON',extensions:['json']}],properties:['openFile']});if(r.canceled)return null;if(path.basename(r.filePaths[0])!=='storyboard.json')throw Error('Pilih fail storyboard.json.');selected=loadProject(path.dirname(r.filePaths[0]));return selected;});
 bind('open',async()=>{if(job)throw Error('Tunggu penjanaan selesai.');await browser.speech();return {message:'Tetingkap dibuka. Login sendiri; pembukaan sahaja tidak mengesahkan login.'};});
 bind('check',async()=>{if(job)throw Error('Penjanaan sedang berjalan.');const r=await browser.prepareSpeech();return {ready:r.ready,message:r.ready?'Editor pertuturan dikesan. Pilihan Ludo akan disemak semasa penjanaan.':r.message};});
 bind('cancel',()=>{job?.abort();return {message:'Permintaan berhenti diterima.'};});
 bind('generate',async()=>{
  if(job||!selected)throw Error('Pilih projek dahulu; satu penjanaan pada satu masa.');
  const ready=await browser.prepareSpeech();if(!ready.ready)throw Error(ready.message);
  const project=loadProject(selected.root);if(project.revision!==selected.revision)throw Error('Storyboard berubah; pilih dan semak semula.');
  const approval=await dialog.showMessageBox(control,{type:'question',buttons:['Batal','Luluskan dan jana Ludo'],defaultId:0,cancelId:0,title:'Hantar narasi ke Google AI Studio?',message:`${project.scenes.length} babak, ${project.scenes.reduce((n,s)=>n+s.narration.length,0)} aksara narasi akan dihantar.`,detail:'Hanya teks narasi dan gaya suara. Login, kuota dan pilihan Ludo diperlukan. Semak teks yang dipaparkan sebelum meluluskan.'});
  if(approval.response!==1)return {message:'Dibatalkan; tiada narasi dihantar.'};
  job=new AbortController();try{const r=await generate(project,browser,{signal:job.signal,onProgress:t=>{if(!control.isDestroyed())control.webContents.send('ludo:progress',t);}});return {message:`${r.clips} WAV disimpan dalam audio/. Semak sebutan dan sediakan cues sebenar sebelum render.`};}finally{job=null;}
 });
 control.on('closed',()=>{job?.abort();browser.dispose();app.quit();});
 await control.loadURL(dashboard);
}).catch(()=>{console.error('Aplikasi gagal bermula. Semak paparan desktop dan dependency sistem.');app.exit(1);});
app.on('window-all-closed',()=>{if(!process.argv.includes('--fixture-audit')&&!process.argv.includes('--live-audit'))app.quit();});
