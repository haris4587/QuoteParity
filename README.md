# QuoteParity

**Comparable supplier bids, with GenLayer verifying scope before deterministic cost ranking.**

A buyer commits purchasing requirements, quantity, currency, deadline and a daily delivery cost. Suppliers submit structured prices and a hash-pinned public quote. An Intelligent Contract independently fetches the document and uses validator consensus to decide whether the quote covers each requirement and matches every structured price. Only qualifying offers enter the published ranking formula.

## Deployment

- Network: **GenLayer Studionet**, chain ID **61999**
- Contract: [`0xEE11429C43dA330BEdb61b8dABABE4C3BAF542F7`](https://explorer-studio.genlayer.com/address/0xEE11429C43dA330BEdb61b8dABABE4C3BAF542F7)
- Deployment transaction: [`0x36b560d48ada59ec61ac1064bf9726953a0ed5269275458225f939a361ec1e15`](https://explorer-studio.genlayer.com/tx/0x36b560d48ada59ec61ac1064bf9726953a0ed5269275458225f939a361ec1e15)
- Deployment submitted through **GenLayer Studio's built-in account**, full consensus mode. No external wallet connection.
- Website: publication in progress. See `public/deployment.json` and `docs/live-run.json` for final evidence.

## Workflow

1. **Commit a purchase request.** 1–12 immutable requirements, quantity, currency, bid deadline (30 seconds–30 days ahead), daily delivery cost in integer minor units.
2. **Submit a public quote.** UTF-8 text, JSON or static HTML, at most 32 KB, HTTPS. Commit SHA-256 of the exact decoded UTF-8 document, unit price, delivery total, warranty total, tax total and delivery days. Validators independently fetch and hash the source at submission.
3. **Evaluate scope.** Every validator re-fetches the pinned source. AI classifies each requirement as `covered`, `excluded` or `unclear` and checks structured prices against the quote. The custom equivalence validator independently repeats this task and requires exact normalized agreement. It does not accept the leader's conclusion without checking the public evidence.
4. **Finalize comparison.** After bidding ends, anyone can finalize when all reviews are terminal, or after the 24-hour review timeout. Only `qualified` bids rank. Unresolved bids are excluded, never converted into eligibility.

## Fixed formula

```
landed_cost = quantity × unit_price + delivery + warranty + tax
score = landed_cost + daily_penalty × delivery_days
```

All amounts are integer minor units (100 cents = $1). Delivery, warranty and tax are **order totals**, not per-unit prices. Lowest score wins. Ties break by landed cost, delivery days, then bid ID. There is no currency conversion. The currency label does not implement currency-specific decimal exponents; this version uses two decimal places for all supported UI currencies.

## Trust boundaries

- Requirements and formula cannot be edited after request creation.
- Submission limits: 20 bids/request, 3 bids/address, 100 requests/deployment. These are resource limits, not identity or Sybil prevention.
- Duplicate URL or document digest in one request is disallowed.
- Missing, oversized, non-UTF-8 or changed source is not proof. Review records explicit inconclusive outcomes. A bad hash or unavailable source at submission rejects the transaction.
- At most three review attempts for pending/inconclusive bids. All completed reviews append immutable decision hashes and timestamps.
- Source bodies are treated as untrusted evidence in the prompt. Models may still err; protocol consensus is not a guarantee of legal meaning, supplier identity, delivery, authenticity or honest pricing.
- Qualified/rejected decisions are terminal within this contract. Protocol-level appeals are supplied by GenLayer; no custom buyer override or application appeal is implemented.
- Scope review concerns the pinned document at the review time. It does not continuously monitor a supplier website after qualification.
- This is a **procurement comparison** app. It does not create a legally binding award, send purchase orders, escrow funds or pay suppliers.
- PDF/binary files, dynamic authenticated pages and documents over 32 KB are intentionally unsupported. Use a public text export containing the complete quote terms.

## Run locally

```bash
npm ci
npm test
npm run dev
npm run build
```

Python 3.10+ is required for tests. The frontend uses pinned `genlayer-js@1.1.8`, the stable npm release available at implementation time, and Vite. The SDK's installed source and type declarations are authoritative for the stable Studionet API; newer documentation also describes v2 preview methods not exposed by 1.1.8.

## Wallet and finality

The deployed contract was created through Studio's built-in wallet. The website creates its own **session-only Studionet test account** using the SDK, with Studio's test faucet RPC. No external wallet connection, mainnet assets or seed phrase are requested. Keys stay in the current tab's `sessionStorage`; closing the browser session clears them. Do not use this development-only wallet for real assets. A new tab/account does not control prior buyer identities, but requests are immutable and reviews/finalization are permissionless.

Writes call the real deployed contract with a local signing account, persist the transaction ID before waiting, and verify `FINALIZED` **and** `FINISHED_WITH_RETURN`. Pending IDs can be resumed rather than blindly resubmitted. Reads explicitly select `TransactionHashVariant.LATEST_FINAL`.

## Tests

`npm test` runs deterministic Python contract tests with an SDK-shaped harness. Tests cover creation → submission → qualification → final ranking, exclusions, price mismatch, unavailable/changed sources, hash mismatch, deadlines, bounded retries, no post-finalization changes, duplicate limits, integer validation, formula arithmetic and tie-breaking. These mock tests do **not** execute GenVM or establish LLM accuracy. The live Studionet run is separately documented under `docs/` with real transaction receipts and finalized-state reads.

## API

| Method | Purpose |
|---|---|
| `create_request(title, requirements_json, quantity, currency, deadline, daily_penalty)` | Commit immutable purchasing terms; returns ID |
| `submit_quote(request_id, supplier, url, expected_hash, unit_price, delivery, warranty, tax, delivery_days)` | Commit quote and independently fetch pinned evidence |
| `evaluate_quote(request_id, bid_id)` | Independent validator web/AI scope and price review |
| `finalize_request(request_id)` | Freeze deterministic ranking after deadline/review rules |
| `get_state()` | JSON database for comparison UI |
| `get_request(request_id)` | JSON purchase request with bids and review history |

## Official references checked

- [Web-response SDK declaration](https://github.com/genlayerlabs/genvm/blob/main/runners/genlayer-py-std/src/genlayer/nondet/web.py): `Response.status`, `headers`, `body`. Some web documentation examples still use `status_code`; QuoteParity follows the declared SDK.
- [Non-determinism](https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism)
- [Reading data](https://docs.genlayer.com/developers/decentralized-applications/reading-data)
- [Writing data](https://docs.genlayer.com/developers/decentralized-applications/writing-data)
- [Studio](https://docs.genlayer.com/developers/intelligent-contracts/tools/genlayer-studio)

The public quote fixtures in `public/quotes/` are explicitly fictional test evidence, not real supplier offers.
