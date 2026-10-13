# QuoteParity — comparable supplier bids

QuoteParity uses GenLayer to assess documented supplier scope and exclusions, then ranks qualifying bids using immutable purchasing terms and integer arithmetic. Supplier names are **unverified claims**. Wallet signatures establish wallet control, not authority to represent a company.

- Public app: https://quoteparity.itzanza2.chatgpt.site
- Repository: https://github.com/haris4587/QuoteParity
- Current contract: https://explorer-studio.genlayer.com/address/0xBA2212A111f5e59d64A4F9d2E1217bF93903Fbf7
- Full Consensus deployment: https://explorer-studio.genlayer.com/tx/0xfd57b095db158a4c55ad28bcc9bbe3a202245104c64e3800e7940f8910c6c2aa
- Network: stable Studionet, chain ID 61999, RPC https://studio.genlayer.com/api, genlayer-js 1.1.8.

## Main workflow

1. Use **Create test account** in the app. It generates a session-only test signer and uses the Studionet faucet; no external wallet extension is connected. Use **Account address** to share a supplier's public address with the buyer. Private keys are never exported in the evidence.
2. A separate buyer account creates a purchase request, committing requirements, quantity, currency, bid/review deadlines, delivery-time cost and an immutable roster of 1–20 invited supplier wallets. The buyer cannot also be a supplier in that request. Roster admission is buyer curation, not corporate authentication.
3. Each invited wallet owns one reserved active slot and can submit at most three successful quotes. Uninvited Sybil wallets cannot consume capacity; one invited wallet cannot consume another's slot. Failed source/hash admission does not use an attempt. A new valid submission supersedes only that sender's previous bid, preserving its history.
4. Suppliers submit structured integer prices and a public document's SHA-256. Validators independently retrieve it during admission and again during assessment. Supported evidence is UTF-8 text, JSON or static HTML, 1–32,000 bytes. Pin normal evidence to a version; a deliberately mutable fixture is used only for the source-change test.
5. Any account can request an independent validator assessment. Each committed requirement is `covered`, `excluded` or `unclear`; price consistency is Boolean. All decision-critical normalized fields require strict agreement. A quote qualifies only with unchanged evidence, full coverage and matching prices.
6. After the bid deadline, anyone can finalize when active reviews are resolved or exhausted. Unresolved bids can hold finalization only until the committed 24-hour review timeout; they never qualify automatically. Review attempts are bounded to three per bid. Only active qualifying bids rank.

## Published arithmetic

All prices use currency minor units (100 cents = 1 USD).

```
landed_cost = quantity * unit_price + delivery + warranty + tax
score = landed_cost + daily_penalty * delivery_days
rank key = score, landed_cost, delivery_days, bid_id
```

The formula and tie-breakers are committed before quotes. Ranking does not place an order, transfer funds or make a legal procurement award. No escrow is implemented or needed for the documented scope.

## Verified live main comparison

Request #0 was created, populated, evaluated and finalized through the public app's signed transaction interface, using a separate buyer and six separate supplier wallets. Full Consensus was used for deployment and live writes; finalized receipts include GenVM results and validator votes. A read-only verification script checks latest-final network state and exact deployed-source equality.

| Final rank | Claimed supplier | Landed cost | Days | Score | Result |
|---|---|---:|---:|---:|---|
| 1 | Zephyr | $8,900 | 5 | $8,950 | qualified |
| 2 | Twin | $8,900 | 5 | $8,950 | qualified |
| 3 | Meridian | $8,990 | 8 | $9,070 | qualified |
| 4 | Atlas | $9,000 | 7 | $9,070 | qualified |
| — | Unclear | $8,600 | 4 | $8,640 | rejected |
| — | Budget | $8,000 | 3 | $8,030 | rejected |

Exact ranking is `[2,3,1,0]`. Zephyr/Twin use bid-ID tie-breaking; Meridian/Atlas use lower landed cost at equal score. The intended ambiguous-warranty wording was actually classified as excluded by live validators; it is recorded as rejected, never relabeled as inconclusive. A separate incomplete-warranty test exercises conservative inconclusive handling. The mutable-source experiments returned unchanged cached content and qualified; they are not claimed as successful live source-change tests.

The wrong-hash transaction failed without consuming a supplier attempt; that wallet subsequently submitted successfully. An uninvited Studio wallet failed admission while legitimate suppliers could participate. Incomplete-evidence review and finite retry exhaustion are documented in [the steward report](docs/STEWARD-REVISION.md).

## Live inconclusive recovery and delivery tie

Request #2 was created by a new independent buyer with three reserved supplier wallets. The two active qualifiers each cost $9,000 with zero delivery penalty: Fast delivers in 5 days and Atlas in 7 days. Final ranking `[2,1]` selects Fast by delivery duration. A third wallet replaced its own earlier offer with version-pinned incomplete warranty evidence; the earlier quote retains its history and is superseded. Three independent reviews remain INCONCLUSIVE, and finalization excludes that unresolved quote. Legitimate participation and ranking both remain possible. See [actual live report](docs/STEWARD-REVISION.md).

## Error handling and trust limits

- Malformed/oversized JSON, missing/extra fields, wrong types and invalid scope arrays produce conservative structured outcomes. Model exceptions and unavailable, oversized, non-UTF-8 or changed sources cannot qualify.
- Each validator performs its own source fetch and assessment. Untrusted documents are evidence, never instructions. Hash commitments prove content equality, not supplier truthfulness or delivery performance.
- This is a buyer-invited comparison, not an open marketplace. Invitations must be arranged outside the contract. The buyer chooses the immutable roster; the contract does not verify company authority.
- Limits: 100 requests per deployment, 20 invited wallets per request, three accepted submissions per wallet, three reviews per bid, at most 60 archived bids / 20 current bids per request. Evidence portals requiring authentication, PDFs and dynamic browser rendering are unsupported.
- All supplier fixtures are fictional. Studionet has temporary development-state availability; this is not a production purchasing system.

## Development and evidence

```
npm ci
npm test
npm run build
npm run dev
```

Tests use an SDK-shaped deterministic mock harness plus JSDOM; they supplement real network executions and do not replace them. GenVM AST lint and SDK semantic validation pass with the pinned runner. See [validation](docs/VALIDATION.md), [current state](docs/revision2-state.json), [verification](docs/revision2-verification.json), [schema](docs/revision2-schema.json) and [finalized receipts](docs/revision2-receipts).

`scripts/verify-revision2.mjs <transaction hashes...>` performs read-only RPC verification. It submits no transactions. `public/deployment.json`, the live-source download and `contracts/quote_parity.py` identify the same deployed revision. Historical October 3 evidence is preserved as baseline evidence.

Official API references: [web access](https://docs.genlayer.com/developers/intelligent-contracts/features/web-access), [calling LLMs](https://docs.genlayer.com/developers/intelligent-contracts/features/calling-llms), [non-determinism](https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism), [networks](https://docs.genlayer.com/developers/networks), [GenVM linter](https://docs.genlayer.com/api-references/genlayer-linter).
