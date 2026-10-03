// Stable Studionet and protocol receipts have different execution envelopes.
export function executionSucceeded(receipt){
  if(receipt.txExecutionResultName!==undefined)return receipt.txExecutionResultName==='FINISHED_WITH_RETURN';
  const raw=receipt.consensus_data?.leader_receipt??receipt.consensusData?.leader_receipt;
  const leaders=Array.isArray(raw)?raw:raw?[raw]:[];
  const leader=leaders.find(x=>x.mode==='leader')??leaders[0];
  return leader?.execution_result==='SUCCESS' && (!leader.result || leader.result.status==='return');
}
export function executionDescription(receipt){
  const raw=receipt.consensus_data?.leader_receipt??receipt.consensusData?.leader_receipt;
  const leader=Array.isArray(raw)?raw.find(x=>x.mode==='leader')??raw[0]:raw;
  return receipt.txExecutionResultName??leader?.result?.payload??leader?.execution_result??'Unrecognized execution receipt';
}
