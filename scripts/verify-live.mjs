import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {TransactionHashVariant} from 'genlayer-js/types';
import fs from 'node:fs/promises';
import {executionSucceeded,executionDescription} from '../src/receipt.js';
const config=JSON.parse(await fs.readFile('public/deployment.json','utf8'));
const client=createClient({chain:studionet});
const state=JSON.parse(await client.readContract({address:config.address,functionName:'get_state',args:[],transactionHashVariant:TransactionHashVariant.LATEST_FINAL}));
await fs.writeFile('docs/finalized-state.json',JSON.stringify(state,null,2)+'\n');
for(const hash of process.argv.slice(2)){
 const r=await client.getTransaction({hash});
 const safe={hash,from:r.from_address,to:r.to_address,status:r.statusName,successful:executionSucceeded(r),execution:executionDescription(r),consensus:r.consensus_data?.final?{votes:r.consensus_data.final.votes}:undefined,method:r.data?.calldata?.readable??null};
 console.log(JSON.stringify(safe));
 await fs.mkdir('docs/receipts',{recursive:true});
 await fs.writeFile(`docs/receipts/${hash}.json`,JSON.stringify({...safe,leader_receipts:r.consensus_data?.leader_receipt?.map(x=>({mode:x.mode,execution_result:x.execution_result,result:x.result,genvm_result:x.genvm_result})),votes:r.consensus_data?.votes,leader_only:r.leader_only},null,2)+'\n');
}
console.log(JSON.stringify({requests:state.requests.map(r=>({id:r.id,title:r.title,deadline:r.deadline,closed:r.closed,bids:r.bids.map(b=>({id:b.id,status:b.status,history:b.history,score:b.score})),ranking:r.ranking}))}));
