import test from 'node:test';
import assert from 'node:assert/strict';
import {JSDOM} from 'jsdom';
import fs from 'node:fs/promises';
import JSONbig from 'json-bigint';
import {executionSucceeded} from '../src/receipt.js';

const deployment=JSON.parse(await fs.readFile('public/deployment.json','utf8'));
const request={id:0,title:'Laptop scope test',currency:'USD',quantity:10,deadline:1900000000,review_deadline:1900086400,daily_penalty:1000,requirements:['Delivery','Warranty'],terms_hash:'a'.repeat(64),closed:false,ranking:[],bids:[{id:0,supplier:'Atlas',status:'qualified',unit_price:90000,delivery:0,warranty:0,tax:0,landed_cost:900000,score:907000,delivery_days:7,url:'https://quotes.example/atlas',document_hash:'b'.repeat(64),history:[{status:'qualified',result:{scope:['covered','covered'],prices_match:true,source:'unchanged'}}]}]};
const source=(await fs.readFile('src/main.js','utf8')).replace(/^import .*;\n/gm,'');
async function setup(large=false){
 const dom=new JSDOM('<div id="app"></div>',{url:'https://quoteparity.example'});
 dom.window.HTMLDialogElement.prototype.showModal=function(){this.open=true};dom.window.HTMLDialogElement.prototype.close=function(){this.open=false};
 const calls=[];const account={address:'0x'+'1'.repeat(40)};dom.window.sessionStorage.setItem('quoteparity-session-key','test-key-only');
 const client={readContract:async call=>{calls.push({kind:'read',...call});return JSON.stringify({requests:[request]}).replace('907000',large?'100000000000000123':'907000')},writeContract:async call=>{calls.push({kind:'write',...call});return '0x'+'2'.repeat(64)},waitForTransactionReceipt:async()=>({txExecutionResultName:'FINISHED_WITH_RETURN'}),request:async()=>null};
 const fn=new (Object.getPrototypeOf(async function(){}).constructor)('document','sessionStorage','location','window','fetch','createClient','createAccount','generatePrivateKey','studionet','TransactionHashVariant','TransactionStatus','executionSucceeded','executionDescription','JSONbig',source+'\nreturn {write,createDialog,detail};');
 const api=await fn(dom.window.document,dom.window.sessionStorage,dom.window.location,dom.window,async()=>({json:async()=>deployment}),options=>{calls.push({kind:'client',options});return client},()=>account,()=> 'test-key-only',{}, {LATEST_FINAL:'latest-final'},{FINALIZED:'FINALIZED'},executionSucceeded,()=> 'error',JSONbig);return{dom,calls,api,account};
}
test('application reads finalized state and renders real scope and integer cost',async()=>{const{dom,calls}=await setup();assert.equal(calls.find(c=>c.kind==='read').transactionHashVariant,'latest-final');assert.match(dom.window.document.querySelector('#board').textContent,/Laptop scope test/);assert.match(dom.window.document.querySelector('table').textContent,/\$9,070.00/)});
test('write includes signing client, deployed address and no procurement value',async()=>{const{calls,api}=await setup();await api.write('evaluate_quote',[0,0]);const c=calls.find(c=>c.kind==='write');assert.ok(calls.some(x=>x.kind==='client'&&x.options.account));assert.equal(c.address,deployment.address);assert.equal(c.value,0n);assert.deepEqual(c.args,[0,0]);assert.equal(c.functionName,'evaluate_quote')});
test('quote inspection exposes source review and hash without invented eligibility',async()=>{const{dom,api}=await setup();api.detail(request,request.bids[0]);assert.match(dom.window.document.querySelector('#modal-content').textContent,/Confirmed/);assert.match(dom.window.document.querySelector('#modal-content').textContent,/unchanged/);assert.equal(dom.window.document.querySelector('#review').disabled,true)});
test('success handling ignores cancelled validators but requires leader return',()=>{assert.equal(executionSucceeded({consensus_data:{leader_receipt:[{mode:'leader',execution_result:'SUCCESS',result:{status:'return'}},{mode:'validator',execution_result:'ERROR',result:{status:'contract_error',payload:'idle'}}]}}),true);assert.equal(executionSucceeded({consensus_data:{leader_receipt:[{mode:'leader',execution_result:'ERROR',result:{status:'contract_error'}}]}}),false);assert.equal(executionSucceeded({txExecutionResultName:'FINISHED_WITH_ERROR'}),false)});
test('retained failed live request is not considered success despite finalization',async()=>{const r=JSON.parse(await fs.readFile('docs/receipts/0x93fa522c6ce135b5c002ceb8511d3f358f1992981491541accecd55222a927c2.json'));assert.equal(r.statusName,'FINALIZED');assert.equal(r.leader_receipts[0].execution_result,'ERROR');assert.equal(executionSucceeded({consensus_data:{leader_receipt:r.leader_receipts}}),false)});

test('large integer quote totals retain every cent',async()=>{const{dom}=await setup(true);assert.match(dom.window.document.querySelector('table').textContent,/\$1,000,000,000,000,001\.23/)});
