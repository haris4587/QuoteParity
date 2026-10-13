# QuoteParity steward revision — prepared, deployment pending

2026-10-13. This is a work-in-progress revision, not a claim that all steward requirements are complete. The public app remains configured for the original deployed contract at 0x52Bf9E533159ed35Bc473180b1C86908fFD67883, chain 61999. `public/quote_parity.py` retains that deployment's exact source. `contracts/quote_parity.py` is the proposed revision and has not been deployed.

## Completed source work

- Supplier names are explicitly **unverified claims**, in the contract's new records, request policy, app header, supplier table, submission dialog and inspection. A signature establishes wallet control, not authority to represent a company. Buyer invitations are admission permissions, not corporate verification.
- Requests commit an immutable roster of 1–20 distinct, nonzero supplier wallets; the buyer wallet cannot participate as a supplier. Each invited address has its own reserved slot. Any number of uninvited Sybil wallets cannot consume a slot. Buyer curation is an explicit trust assumption; this is a closed invitation comparison rather than a permissionless marketplace.
- Each invited wallet can submit up to three successful quotes, with only its latest quote current. Failed admission/source/hash validation does not consume an attempt or supersede a valid offer. New submissions supersede the sender's prior offer without deleting evidence or verdict history. Document duplication across wallets cannot steal another wallet's reservation.
- At most 60 history entries / 20 active quotes per request. One malicious invited wallet cannot consume another's allowance. Permissionless finalization excludes unresolved evidence after the committed 24-hour review timeout, so unresolved bids cannot permanently block ranking.
- Invalid JSON, oversized output, wrong types, extra keys, missing keys and malformed scope arrays return structured conservative `invalid_model_output` results. Provider exceptions produce `model_unavailable`; web exceptions produce `source_unavailable`. Qualifying conclusions still require strict agreement with an independent validator assessment.
- Frontend supports revision-two roster creation and reserved-slot admission when `protocolVersion: 2` is activated; its legacy ABI remains active until a matching new deployment is configured.
- Full-page procurement SVG artwork and the supplied Originkit Particle Drift component, adapted to vanilla JavaScript, add subtle animation and scroll parallax. Reduced motion disables movement; background layers do not intercept input. URL is unchanged and access is public.

## Checks

30 deterministic Python contract tests and 10 frontend tests pass. These are SDK-shaped mocked tests, not live GenVM execution. GenVM linter 0.11.0 AST lint and SDK semantic validation pass; output is recorded in revision2-genvm-check.json. The production Vite build passes. The managed preview's control-browser skill is unavailable. After publication, the explicitly requested public app was inspected in the cloud browser: it loaded without sign-in, displayed the new backdrop and unverified identity labels, and loaded request #0 from finalized RPC state. This verifies the desktop public view, not the pending revision-two writes. Screenshot: public-design-proof.jpg.

## Still required before resubmission

Automatic approval review rejected opening Studio for deployment because it interpreted the later design-only instruction as restricting contract changes. No alternative deployment route was used. Clarification is needed to deploy the prepared revision and activate its matching config.

Then run live independent buyer and supplier-wallet transactions through the public app: buyer creates an immutable roster; four qualifying bids with distinct prices/durations, an excluded bid, and an ambiguous bid; uninvited/wrong-hash rejected calls; independent validator evaluations; three conservative reviews of ambiguity or timeout; deterministic final ranking. Use the fixtures in revision2-fixtures.json with commit-pinned public URLs. Do not present their expected results as actual execution.

Expected main comparison requirements: 10 new laptops each with 16 GB RAM and 512 GB SSD; delivery to buyer office within 10 days included; 24-month parts and labour warranty included. Quantity 10, USD, penalty 1000 cents/day. Four qualifying scores: Zephyr 895000, Twin 895000, Meridian 907000, Atlas 907000. Expected rank by bid IDs for submission order Atlas, Meridian, Zephyr, Twin, Budget, Unclear: [2,3,1,0]. The exact Zephyr/Twin tie uses bid ID; Meridian/Atlas score tie uses lower landed cost. Also test penalty=0 with equal landed cost and different delivery days to exercise the delivery tie-break.

Archive finalized GenVM leader results and independent validator votes, rejected call receipts, latest-final authoritative readbacks, source equality from getContractCode, ABI/schema and chain/config equality, app transaction evidence and screenshots. Update live-run.json only after these checks. Existing October 3 live evidence remains historical baseline evidence and does not prove the new revision.

Production design deployment succeeded on 2026-10-13 at the unchanged public URL; Site version 2, source commit fc47f4cb200212ce7fb0bcbf8864dfbc91a4530c. A separate read-only SDK check confirmed chain ID 61999, request #0 ranking [0], and exact byte equality between getContractCode(address) and public/quote_parity.py. These checks concern the original deployment, not the pending revision.
