const {contextBridge,ipcRenderer}=require('electron');
contextBridge.exposeInMainWorld('ludo',{
 choose:()=>ipcRenderer.invoke('ludo:choose'),open:()=>ipcRenderer.invoke('ludo:open'),check:()=>ipcRenderer.invoke('ludo:check'),generate:()=>ipcRenderer.invoke('ludo:generate'),cancel:()=>ipcRenderer.invoke('ludo:cancel'),
 onProgress:fn=>ipcRenderer.on('ludo:progress',(_e,value)=>fn(value))
});
