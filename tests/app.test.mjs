import test from 'node:test';
import assert from 'node:assert/strict';
import {JSDOM} from 'jsdom';
import fs from 'node:fs/promises';
import JSONbig from 'json-bigint';
import {executionSucceeded} from '../src/receipt.js';

const deployment=JSON.parse(await fs.readFile('public/deployment.json','utf8'));
const request={id:0,title:'Laptop scope test',currency:'USD',quantity:10,deadline:1900000000,review_deadline:1900086400,daily_penalty:1000,requirements:['Delivery','Warranty'],terms_hash:'a'.repeat(64),closed:false,ranking:[],bids:[{id:0,supplier:'Atlas',status:'qualified',unit_price:90000,delivery:0,warranty:0,tax:0,landed_cost:900000,score:907000,delivery_days:7,url:'https://quotes.example/atlas',document_hash:'b'.repeat(64),history:[{status:'qualified',result:{scope:['covered','covered'],prices_match:true,source:'unchanged'}}]}]};
const source=(await fs.readFile('src/main.js','utf8')).replace(/^import .*;\n/gm,'');
async function setup(large=false,revision2=false){
 const stateRequest=structuredClone(request);if(revision2){stateRequest.supplier_wallets=['0x'+'1'.repeat(40)];stateRequest.active_bids={};stateRequest.bids[0].superseded_by=null;stateRequest.bids[0].sender='0x'+'1'.repeat(40)}
 const dom=new JSDOM('<div id="app"></div>',{url:'https://quoteparity.example'});
 dom.window.HTMLDialogElement.prototype.showModal=function(){this.open=true};dom.window.HTMLDialogElement.prototype.close=function(){this.open=false};
 dom.window.matchMedia=()=>({matches:true});
 const calls=[];const account={address:'0x'+'1'.repeat(40)};dom.window.sessionStorage.setItem('quoteparity-session-key','test-key-only');
 const client={readContract:async call=>{calls.push({kind:'read',...call});return JSON.stringify({requests:[stateRequest]}).replace('907000',large?'100000000000000123':'907000')},writeContract:async call=>{calls.push({kind:'write',...call});return '0x'+'2'.repeat(64)},waitForTransactionReceipt:async()=>({txExecutionResultName:'FINISHED_WITH_RETURN'}),request:async()=>null};
 const fn=new (Object.getPrototypeOf(async function(){}).constructor)('document','sessionStorage','location','window','fetch','createClient','createAccount','generatePrivateKey','studionet','TransactionHashVariant','TransactionStatus','executionSucceeded','executionDescription','JSONbig',source+'\nreturn {write,createDialog,detail,bidDialog};');
 const api=await fn(dom.window.document,dom.window.sessionStorage,dom.window.location,dom.window,async()=>({json:async()=>({...deployment,protocolVersion:revision2?2:1})}),options=>{calls.push({kind:'client',options});return client},()=>account,()=> 'test-key-only',{}, {LATEST_FINAL:'latest-final'},{FINALIZED:'FINALIZED'},executionSucceeded,()=> 'error',JSONbig);return{dom,calls,api,account};
}
test('application reads finalized state and renders real scope and integer cost',async()=>{const{dom,calls}=await setup();assert.equal(calls.find(c=>c.kind==='read').transactionHashVariant,'latest-final');assert.match(dom.window.document.querySelector('#board').textContent,/Laptop scope test/);assert.match(dom.window.document.querySelector('table').textContent,/\$9,070.00/)});
test('write includes signing client, deployed address and no procurement value',async()=>{const{calls,api}=await setup();await api.write('evaluate_quote',[0,0]);const c=calls.find(c=>c.kind==='write');assert.ok(calls.some(x=>x.kind==='client'&&x.options.account));assert.equal(c.address,deployment.address);assert.equal(c.value,0n);assert.deepEqual(c.args,[0,0]);assert.equal(c.functionName,'evaluate_quote')});
test('quote inspection exposes source review and hash without invented eligibility',async()=>{const{dom,api}=await setup();api.detail(request,request.bids[0]);assert.match(dom.window.document.querySelector('#modal-content').textContent,/Confirmed/);assert.match(dom.window.document.querySelector('#modal-content').textContent,/unchanged/);assert.equal(dom.window.document.querySelector('#review').disabled,true)});
test('success handling ignores cancelled validators but requires leader return',()=>{assert.equal(executionSucceeded({consensus_data:{leader_receipt:[{mode:'leader',execution_result:'SUCCESS',result:{status:'return'}},{mode:'validator',execution_result:'ERROR',result:{status:'contract_error',payload:'idle'}}]}}),true);assert.equal(executionSucceeded({consensus_data:{leader_receipt:[{mode:'leader',execution_result:'ERROR',result:{status:'contract_error'}}]}}),false);assert.equal(executionSucceeded({txExecutionResultName:'FINISHED_WITH_ERROR'}),false)});
test('retained failed live request is not considered success despite finalization',async()=>{const r=JSON.parse(await fs.readFile('docs/receipts/0x93fa522c6ce135b5c002ceb8511d3f358f1992981491541accecd55222a927c2.json'));assert.equal(r.statusName,'FINALIZED');assert.equal(r.leader_receipts[0].execution_result,'ERROR');assert.equal(executionSucceeded({consensus_data:{leader_receipt:r.leader_receipts}}),false)});

test('large integer quote totals retain every cent',async()=>{const{dom}=await setup(true);assert.match(dom.window.document.querySelector('table').textContent,/\$1,000,000,000,000,001\.23/)});

test('supplier identity is explicitly unverified in table and inspection',async()=>{const{dom,api}=await setup();assert.match(dom.window.document.querySelector('#board').textContent,/Unverified supplier claim/);api.detail(request,request.bids[0]);assert.match(dom.window.document.querySelector('#modal-content').textContent,/No company authorization is established/)});
test('revision two exposes immutable reserved supplier slots and new request roster',async()=>{const{dom,api}=await setup(false,true);assert.match(dom.window.document.querySelector('#board').textContent,/reserved slots/);api.createDialog();assert.ok(dom.window.document.querySelector('[name=suppliers]'));assert.match(dom.window.document.querySelector('#modal-content').textContent,/roster is immutable/)});
test('legacy deployment preserves the original create ABI',async()=>{const{dom,api}=await setup();api.createDialog();assert.equal(dom.window.document.querySelector('[name=suppliers]'),null)});
test('background artwork stays decorative and leaves the transaction mount present',async()=>{const html=await fs.readFile('index.html','utf8');const dom=new JSDOM(html);assert.equal(dom.window.document.querySelector('.background-scene').getAttribute('aria-hidden'),'true');assert.ok(dom.window.document.querySelector('#app'));assert.ok(dom.window.document.querySelector('#background-particles'));const css=await fs.readFile('src/style.css','utf8');assert.match(css,/prefers-reduced-motion:reduce/);assert.match(css,/pointer-events:none/)});


test('archived qualified quotes retain history without a final rank',async()=>{
 const original=structuredClone(request);
 try{
  request.closed=true;request.ranking=[1];
  request.bids[0].superseded_by=1;
  request.bids.push({...structuredClone(request.bids[0]),id:1,supplier:'Current',superseded_by:null});
  const {dom}=await setup();
  const rows=[...dom.window.document.querySelectorAll('tbody tr')];
  assert.match(rows.find(r=>r.textContent.includes('Current')).textContent,/qualified · #1/);
  const archived=rows.find(r=>r.textContent.includes('Atlas')).textContent;
  assert.match(archived,/Superseded quote/);assert.doesNotMatch(archived,/#0|qualified · #/);
 }finally{Object.assign(request,original)}
});
