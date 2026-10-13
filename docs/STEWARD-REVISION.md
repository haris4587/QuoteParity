# QuoteParity steward revision — completed deployment and live verification

13 October 2026. Current contract: **0xBA2212A111f5e59d64A4F9d2E1217bF93903Fbf7**, stable Studionet chain **61999**, protocolVersion **2**. Public app: https://quoteparity.itzanza2.chatgpt.site. Deployment used Studio's built-in wallet and Full Consensus; expanded writes used the public app's signed transaction interface with independent development test signers. No external wallet extension was connected and no private keys are recorded.

## Steward requirements and actual evidence

| Requirement | Implementation and verification |
| --- | --- |
| Supplier authentication or unverified identities | Supplier names are unverified claims in contract records, request identity policy, app header, comparison rows, submission dialog and inspection. Wallet control does not authenticate company representation. |
| Prevent Sybil capacity exhaustion | Immutable buyer-selected roster of 1–20 nonzero distinct supplier wallets, excluding buyer. Each wallet owns its reserved slot and three accepted submissions; no global first-come slot competition. Live uninvited call failed and invited suppliers continued. Unit tests exercise many uninvited wallets and all 20 suppliers / 60 bounded history records. Buyer curation is a documented trust assumption. |
| Invalid bids cannot permanently block participation | Invalid admission/hash does not consume an attempt or supersede a valid quote. Replacements affect only that sender, preserve history and exclude the predecessor. Unit adversarial tests cover replacements and simulated 24-hour timeout. Live request #2 admitted legitimate offers while another wallet held its own slot; after three inconclusive reviews ranking finalized with that offer excluded. |
| Separate buyer and suppliers | Request #0 buyer 0x64F7F82113cA72582aE1B35DE4daA6545BCDF4B2 and six different supplier wallets. Request #2 buyer 0x2c21D725448c27217969C88CE4f43F22792DE267 and three different supplier wallets. Authoritative state records the roster and every sender. |
| Multiple qualifying quotes, prices and durations | Request #0 four qualifiers: Zephyr $8,900 / 5 days / $8,950 score; Twin same; Meridian $8,990 / 8 days / $9,070 score; Atlas $9,000 / 7 days / $9,070 score. Final ranking [2,3,1,0]. |
| Deterministic ties | Request #0 resolves Zephyr/Twin exact tie by bid ID and Meridian/Atlas equal score by landed cost. Request #2 uses daily_penalty=0, equal landed cost/score $9,000, Fast 5 days before Atlas 7 days; final ranking [2,1]. |
| Rejected submissions | Request #0 wrong-hash and uninvited writes finalized with contract errors. Budget's corrected submission succeeded and independent assessment rejected explicit scope exclusions. The first ambiguous wording was also rejected; it is never relabeled inconclusive. Request #2 retained a separate failed hash admission caused by an extra newline in fixture bytes; corrected exact-byte hash succeeded. |
| Inconclusive evidence | Request #2 bid #3 uses a commit-pinned document that does not determine warranty coverage. All three finalized reviews return scope [covered,covered,unclear], prices_match=true and status inconclusive. Finalization excludes it; no automatic qualification occurs. |
| Malformed model responses | JSON parsing is guarded, oversized output bounded, and exact keys/types/array shape checked. Malformed JSON and bad schemas return structured invalid_model_output with unclear scope and false prices_match. Injected provider failures and malformed output are tested deterministically; live model output was not forced to be malformed. |
| Public transaction interface | Public app opened without sign-in. UI generated/funded separate test accounts, created requests, submitted quotes, invoked independent consensus and finalized ranking. Session keys remain in browser sessions. Screenshots and 36 finalized receipt records corroborate the path. |
| Final GenVM/state/configuration | All 36 archived calls are FINALIZED, including three intentional/retained rejected admissions. Each receipt includes leader GenVM results and validator votes. Source equality and chain/protocol equality pass. State is read with LATEST_FINAL, not pending state. ABI is retained. |
| Scope without escrow | No order placement, purchasing-fund transfer, payment settlement or escrow. All test suppliers are fictional. |

## Final request #2 recovery state

The initial mutable-source bid #0 has superseded_by=3 and retains its prior qualifying history. Bid #1 Atlas and bid #2 Fast remain independent qualifying offers. Bid #3 Undetermined warranty is inconclusive with exactly three review records. Active-slot count remains three. Final ranking is [2,1], closed=true; unresolved evidence is excluded. The app disabled finalization before retry exhaustion and enabled it afterward. The 24-hour fallback for a participant who never requests reviews is covered by a simulated-time adversarial test.

## Honest experiment limits

Request #1 and the initial mutable-source experiment in request #2 were intended to exercise source-change handling. Despite GitHub changing, GenVM returned the original committed bytes; assessments were qualified with source=unchanged. This is consistent with an upstream/GenVM cached response, but the cause is not established. These calls are preserved and **do not prove live source-change detection**. The source hash mismatch branch is covered by deterministic tests; the live inconclusive evidence is the separate version-pinned missing-warranty fixture.

The 24-hour timeout and malformed-model cases are deterministic adversarial tests, not claims of injected live failures. Independent validator votes can include idle cancellations after quorum; receipts retain those results transparently. Historical October 3 transactions remain baseline evidence.

## Files and checks

- 42 tests pass: 31 Python contract, 11 Node/JSDOM frontend/receipt tests. Full-capacity, Sybil, replacement, timeout, malformed-output, arithmetic and archival-rank regressions are included.
- Exact deployed source has passed GenVM AST lint and SDK semantic validation; [output](revision2-genvm-check.json). No contract changes followed deployment.
- [LATEST_FINAL state](revision2-state.json), [source/config equality and finalized results](revision2-verification.json), [ABI](revision2-schema.json), [live manifest](live-run.json), [individual receipts](revision2-receipts).
- [Inconclusive UI proof](revision2-inconclusive-proof.jpg), [finalized ranking UI proof](revision2-final-ranking-proof.jpg).
- Run `node scripts/verify-revision2.mjs --all` to repeat read-only verification and collect all finalized calls. It submits no transactions.
- [Paste-ready resubmission details](SUBMISSION.md). The portal itself has not been resubmitted by this run.

## Finalized live transaction links

| Method | Execution | Explorer |
| --- | --- | --- |
| deploy | success | [receipt](https://explorer-studio.genlayer.com/tx/0xfd57b095db158a4c55ad28bcc9bbe3a202245104c64e3800e7940f8910c6c2aa) |
| create_request | success | [receipt](https://explorer-studio.genlayer.com/tx/0x483fec4ae98ef07c306d386cb1690e33b0db724e5078fb58c066e15c4e7e02e0) |
| submit_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x622f14de1d404bd1bcf1c2dc04554cdaa5ed7a7bab0c493fa640dca74aff9f28) |
| submit_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x3af078a5bfc5236401dd81b5f5a5990cb1aaa6cd56389e57140e396117a3e83e) |
| submit_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0xd669e3c45ed8e4c21a51f1c4071a334c6567ba2feaa0c7692bba0081d35a071f) |
| submit_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x13b7924cad1d1357ae5f259f3ed850cf8b398490a4bf8be2c0b93c27a9370415) |
| submit_quote | document changed or incorrect hash | [receipt](https://explorer-studio.genlayer.com/tx/0xce7b6fed1238fa82922cde5a699aa9698a8eb507d9978ec45b2611cadee04d6c) |
| submit_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x4621a4b9ffc46c3a3e8a4a1c97f7a77bec994603041bc7abc795be7c60fe7b72) |
| submit_quote | supplier wallet not invited | [receipt](https://explorer-studio.genlayer.com/tx/0x22b24b8209f31b427d5b2fd06bfda14521196dd8910689288a1476ae0010c825) |
| submit_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x855d25d9636b9e702803193b7f81287474a283cbe8eb5833abb037498d05385e) |
| evaluate_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x9a326eb4ef96f433edf8105dcc74ecc8aa976f1f064d354c285de6edd88424de) |
| evaluate_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x1e1f7c6e06fe5ec98099df04ff86341c106ccb3f842222efcf9275913ef51d5a) |
| evaluate_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0xdebdd97f8abe8479082249eeb48289af04dc85dd354732fd593ff22d05fe9d87) |
| evaluate_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x0265da3dc8d2311934c67a181dc3d797e90b2fed77ff9365ac57755db85938ed) |
| evaluate_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x74410ed263a5ae896a6a37575c6add58295199402b634e974dd678cbdc7b8dee) |
| evaluate_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0xd8c1c5a67f1d89262e291f661c49c728cd3abc2239745e99557c1f8fe5cc82db) |
| finalize_request | success | [receipt](https://explorer-studio.genlayer.com/tx/0x70335913fec8445d800a0b68bbf15f1e764204c6b2bd9fa24aace419bb7cb1ed) |
| create_request | success | [receipt](https://explorer-studio.genlayer.com/tx/0x2a1e18eb12e2faa6b0837bceea0bd641d3d03bee15dacb6655b947efa08970d2) |
| submit_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x5616cd60eecbbe812bf26cac8feb4cfcea7537b8eb811f498ac4d0af95f33a34) |
| submit_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0xa25069453da3ec87d55f6c33d58e983e12ae1aa021f768ccb7ad13f1c20ba634) |
| evaluate_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0xe50f810a2b414e1b7122da9ca0415cb1860f5de6d9b2b0504416bbb3e4b3d14b) |
| evaluate_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x784289eb3e9a1db5c48a75389d35f846dfc6860c69591d6fe896ba82e8030bf6) |
| create_request | success | [receipt](https://explorer-studio.genlayer.com/tx/0xea92101c7bd2ff6ba9d2bb5f74cec7116fa98bc55c2398a82e2fa82769b4bbe9) |
| finalize_request | success | [receipt](https://explorer-studio.genlayer.com/tx/0x548a901f505a2b44f18e04aa6af05553db8fdf6b64b779e989be22b5807e3069) |
| submit_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x3bc61c6f4f41c362a13f97aed4a1ee593f138afe30fb261d625371dfa209374b) |
| submit_quote | document changed or incorrect hash | [receipt](https://explorer-studio.genlayer.com/tx/0xec93ec9305e5221d183d4bd6401366e89a44a2f962d61027ff6837e013544bdb) |
| submit_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0xb3fadfaecb8618d22636b824c7646b8380ae68151f839c5e96adaefb5fd0ab13) |
| submit_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x628b066d3186e318f56a669b8fe33eb3da5b301473d4cde478ae2d1a470f6b13) |
| evaluate_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x51d4730c4ff25d72a7542fb374e672cfb74ea18d1e29e818bc94619887d37bac) |
| evaluate_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0xb6039e7746e0d215ed47b64023ff627e8e42a87254a6a59797dc8bbaa81be44b) |
| evaluate_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x6d5a4b4ae394c660ce6c0c58bdd747b9d9db4152074963cba3339a30c52b8317) |
| submit_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0xe1ce24b4595fd680f5c1a34eba4f4ddf9399d705bb97f6b845e5ca38095a0338) |
| evaluate_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0xba8086287df022df36e0fc32dccc49165e1d0411a367582da56795452010fc77) |
| evaluate_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0xc427d839fc360904e991df8a198de717c8755c2f83611a2d2ebcf1b1b523b9cb) |
| evaluate_quote | success | [receipt](https://explorer-studio.genlayer.com/tx/0x676f5f159705b5c16d00079efdaf40b460452e0ee5a45c4860ffb545b8594be4) |
| finalize_request | success | [receipt](https://explorer-studio.genlayer.com/tx/0xf2ac503a18b617dde36fb790e77389d7087a84404efbbd7bbc243fb2f376503c) |
