/* Unit tests with mocked browser APIs. Not a replacement for device testing. */
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const site = path.resolve(__dirname, '../docs');
const events = {};
const storage = new Map();
const calls = {claim:0, skipWaiting:0};
const base = 'https://rotacerta.invalid/rotacerta-demo/';
const keyOf = req => typeof req === 'string' ? req : req.url;
function cacheObject(data) {
 return {
   async addAll(requests) {
     const staged=[];
     for(const req of requests) {
       const filename=new URL(keyOf(req)).pathname.replace('/rotacerta-demo/','');
       staged.push([keyOf(req),new Response(fs.readFileSync(path.join(site,filename)))]);
     }
     for(const [key,response] of staged)data.set(key,response);
   },
   async match(req){return data.get(keyOf(req))?.clone();},
   async put(req,response){data.set(keyOf(req),response.clone());}
 };
}
const caches = {
 async open(name){if(!storage.has(name))storage.set(name,new Map());return cacheObject(storage.get(name));},
 async keys(){return [...storage.keys()];},
 async delete(name){return storage.delete(name);}
};
const context=vm.createContext({
 URL,Request,Response,caches,console,
 fetch:async()=>{throw new Error('offline mock');},
 self:{location:{href:base+'sw.js'},clients:{claim:async()=>{calls.claim++;}},skipWaiting:()=>{calls.skipWaiting++;},addEventListener:(event,handler)=>{events[event]=handler;}}
});
vm.runInContext(fs.readFileSync(path.join(site,'sw.js'),'utf8'),context);
async function lifecycle(name){let pending;events[name]({waitUntil:p=>{pending=p;}});await pending;}
async function request(url,mode='navigate',method='GET'){
 let handled=false,pending;
 events.fetch({request:{url,method,mode},respondWith:p=>{handled=true;pending=p;}});
 return {handled,response:await pending};
}
(async()=>{
 const ownOld='rotacerta-pwa:'+encodeURIComponent('/rotacerta-demo/')+':0.9.0';
 storage.set(ownOld,new Map());storage.set('another-app:1',new Map());
 await lifecycle('install');
 assert.equal(calls.skipWaiting,0,'Do not auto-update while a form is in use');
 await lifecycle('activate');
 assert(!storage.has(ownOld));assert(storage.has('another-app:1'));assert.equal(calls.claim,1);
 const home=await request(base);
 assert(home.handled);
 assert((await home.response.text()).includes('rc-auth-form'));
 const css=await request(base+'pwa.css','no-cors');
 assert(css.handled);assert((await css.response.text()).includes('.rc-pwa-profile'));
 assert.equal((await request('https://wa.me/5500000000000')).handled,false);
 assert.equal((await request(base+'api/orders','cors','POST')).handled,false);
 assert.equal((await request('https://rotacerta.invalid/other-project/')).handled,false);
 assert.equal((await request(base+'unrelated.png','no-cors')).handled,false);
 events.message({data:{type:'unknown'}});assert.equal(calls.skipWaiting,0);
 events.message({data:{type:'ROTACERTA_ACTIVATE_UPDATE'}});assert.equal(calls.skipWaiting,1);
 console.log('PASS: asset cache, offline fallback (mocked), scope isolation, update opt-in and external request exclusions.');
})().catch(error=>{console.error(error);process.exitCode=1;});
