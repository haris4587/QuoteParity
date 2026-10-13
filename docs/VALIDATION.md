# Validation — revision 2

- `npm test`: 42 passing tests (31 Python contract tests and 11 Node/JSDOM tests). Covers malformed JSON and schemas, unavailable and changed evidence, 20-wallet capacity with 60 bounded historical bids, uninvited Sybils, per-wallet reservations, failed admissions, replacements, retry exhaustion, the 24-hour unresolved-review timeout, integer arithmetic and all tie-break levels.
- Production build: Vite; final packaging runs the same build against the pushed source.
- GenVM AST lint and SDK semantic validation passed for the exact deployed contract; retained output: [revision2-genvm-check.json](revision2-genvm-check.json). No contract edits occurred after deployment.
- Full Consensus deployment and independent supplier assessments: finalized GenVM results and votes in [revision2-receipts](revision2-receipts). A quorum-cancelled validator may be marked idle/error; it is not an application failure when the leader returned successfully and agreement quorum finalized.
- Read-only verifier checks exact byte equality of `getContractCode`, `contracts/quote_parity.py` and the public source download, chain 61999 and protocolVersion 2. State reads use LATEST_FINAL; records: [revision2-state.json](revision2-state.json), [revision2-verification.json](revision2-verification.json), [revision2-schema.json](revision2-schema.json).
- Public app's transaction interface was used for purchase-request creation, supplier submission, validator evaluation and ranking. Buyer and supplier addresses are distinct. Test signers use session-only keys and the development faucet; no external wallet extension was connected and no keys are published.
- Source-change behavior is verified in deterministic tests. Live mutable-source experiments returned unchanged content after the GitHub source changed; those offers qualified. These experiments are preserved as limitations, not relabeled as inconclusive evidence. A separate version-pinned incomplete-warranty fixture tests the live inconclusive path.
- Malformed model output is injected in deterministic tests; live providers were not forced to emit invalid JSON. The timeout is simulated in tests rather than waiting 24 hours live.
- Historical October 3 evidence is retained as baseline, including failed calls. It does not prove revision 2.

Fixtures are fictional. These checks do not establish company authenticity, legal procurement authority, production readiness or an audit.
