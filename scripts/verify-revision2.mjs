// Read-only verification. All writes in this live run were submitted through the app or Studio UI.
import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {TransactionHashVariant} from 'genlayer-js/types';
import {executionSucceeded,executionDescription} from '../src/receipt.js';
const config=JSON.parse(await fs.readFile('public/deployment.json','utf8'));
const client=createClient({chain:studionet});
const state=JSON.parse(await client.readContract({address:config.address,functionName:'get_state',args:[],transactionHashVariant:TransactionHashVariant.LATEST_FINAL}));
const deployedCode=await client.getContractCode(config.address);
const source=await fs.readFile('contracts/quote_parity.py','utf8');
const publicCode=await fs.readFile('public/quote_parity.py','utf8');
if(deployedCode!==source||source!==publicCode||config.chainId!==studionet.id||config.protocolVersion!==2)throw Error('Source or config mismatch');
await fs.mkdir('docs/revision2-receipts',{recursive:true});
const receipts=[];
let hashes=process.argv.slice(2);
if(hashes.includes('--all')){
 const index=await client.request({method:'sim_getTransactionsForAddress',params:[config.address]});
 hashes=index.filter(t=>t.status==='FINALIZED').map(t=>t.hash).reverse();
}
for(const hash of hashes){
 const r=await client.getTransaction({hash});
 const safe={hash,from:r.from_address,to:r.to_address,status:r.statusName,successful:executionSucceeded(r),execution:executionDescription(r),method:r.data?.calldata?.readable??null,leader_only:r.leader_only,
 leader_receipts:r.consensus_data?.leader_receipt?.map(x=>({mode:x.mode,execution_result:x.execution_result,result:x.result,genvm_result:x.genvm_result})),votes:r.consensus_data?.votes};
 if(safe.status!=='FINALIZED')throw Error('Not finalized: '+hash);
 await fs.writeFile(`docs/revision2-receipts/${hash}.json`,JSON.stringify(safe,null,2)+'\n');receipts.push(safe);
}
await fs.writeFile('docs/revision2-state.json',JSON.stringify(state,null,2)+'\n');
await fs.writeFile('docs/revision2-verification.json',JSON.stringify({checkedAt:new Date().toISOString(),chainId:studionet.id,address:config.address,protocolVersion:config.protocolVersion,sourceMatches:true,publicSourceMatches:true,sourceSha256:createHash('sha256').update(source).digest('hex'),readVariant:'LATEST_FINAL',receipts},null,2)+'\n');
console.log(JSON.stringify({sourceMatches:true,receipts:receipts.length,requests:state.requests.map(r=>({id:r.id,closed:r.closed,ranking:r.ranking,bids:r.bids.map(b=>({id:b.id,status:b.status,history:b.history.length,source:b.history.at(-1)?.result.source}))}))}));
