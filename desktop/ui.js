const $=id=>document.getElementById(id);let busy=false;
async function action(fn){if(busy)return;busy=true;try{const result=await fn();if(result?.error)throw Error(result.error);return result;}catch(e){$('status').textContent=e.message;}finally{busy=false;}}
$('choose').onclick=()=>action(async()=>{const p=await window.ludo.choose();if(!p)return;$('project').textContent=p.title;$('scripts').replaceChildren();for(const s of p.scenes){const a=document.createElement('article'),h=document.createElement('h3'),t=document.createElement('pre');h.textContent=s.id+' — '+s.title;t.textContent=s.narration;a.append(h,t);$('scripts').append(a);}$('generate').disabled=false;$('status').textContent='Semak semua teks sebelum meluluskan.';});
$('open').onclick=()=>action(async()=>{$('status').textContent=(await window.ludo.open()).message;});
$('check').onclick=()=>action(async()=>{$('status').textContent=(await window.ludo.check()).message;});
$('generate').onclick=()=>action(async()=>{$('generate').disabled=true;try{const r=await window.ludo.generate();$('status').textContent=r.message;}finally{$('generate').disabled=false;}});
$('cancel').onclick=()=>window.ludo.cancel();window.ludo.onProgress(t=>$('status').textContent=t);
