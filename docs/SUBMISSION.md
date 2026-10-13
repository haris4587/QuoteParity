# QuoteParity revision 2 resubmission

Replace the original contract link with:
https://explorer-studio.genlayer.com/address/0xBA2212A111f5e59d64A4F9d2E1217bF93903Fbf7

Website remains https://quoteparity.itzanza2.chatgpt.site and is public.

## What did you change? (under 1,000 characters)

Deployed revision 2 and matched the public app to its exact source, ABI and chain 61999. Supplier names are explicitly unverified claims. Immutable buyer-invited wallet rosters reserve one slot per supplier; Sybil wallets cannot consume slots, failed admission uses no attempt, replacements preserve history, and bounded retries/timeouts prevent permanent blocking. Malformed JSON returns structured INCONCLUSIVE. Live app transactions used separate buyer/supplier wallets: four bids qualified with different prices/durations; ranking [2,3,1,0] proves cost and bid-ID ties. Another request finalized [2,1], proving the delivery tie after three INCONCLUSIVE warranty reviews; unresolved and superseded bids were excluded. Wrong-hash and uninvited calls were rejected. 42 tests pass; GenVM lint/SDK validation pass. Finalized GenVM results, validator votes, authoritative state and source/config equality are archived. The unchanged website is public. No escrow is needed.

## Read-only review path

1. Open the public app and click Refresh finalized state. No account is required to inspect finalized results.
2. Select request #0, Steward verification · independent supplier bids. Four qualifying wallets rank Zephyr, Twin, Meridian, Atlas; Budget and the initial ambiguous fixture are rejected.
3. Select request #2, Steward verification · inconclusive recovery and delivery tie. Fast (5 days) ranks above Atlas (7 days) at equal $9,000 cost and score. Inspect Undetermined warranty: warranty is unclear, all three reviews are preserved, status remains inconclusive and it is excluded. The prior quote from that wallet is superseded and excluded.
4. Expand Contract and transaction evidence. The current address and downloaded source match revision 2; Live test record links all 36 finalized transactions.

## Evidence

- [Steward requirement report](STEWARD-REVISION.md)
- [Live transaction manifest](live-run.json)
- [Authoritative latest-final state](revision2-state.json)
- [Source/config/readback verification and GenVM results](revision2-verification.json)
- [Individual finalized receipts and votes](revision2-receipts)
- [Contract ABI](revision2-schema.json)
- [Validation and limits](VALIDATION.md)
- [Live inconclusive screenshot](revision2-inconclusive-proof.jpg)
- [Final ranking screenshot](revision2-final-ranking-proof.jpg)

Historical October 3 evidence is preserved in baseline files. Mutable-source experiments returned unchanged content and qualified, so they are not described as live source-change detection. Malformed model output and the 24-hour timeout are adversarial unit tests. No demo video has been published.
