# QuoteParity — Project Explorer copy

## Name
QuoteParity

## One-liner
GenLayer checks supplier quote scope and exclusions before a committed cost formula ranks comparable bids.

## Overview
QuoteParity helps buyers compare supplier offers on equal terms. A buyer commits purchasing requirements, quantity, currency, deadline and cost formula. Suppliers commit structured prices and public quote document hashes. The Intelligent Contract independently fetches each source and uses validator AI consensus to determine whether it covers the required scope, hides exclusions or disagrees with the submitted prices. Deterministic rules rank only qualifying offers by landed cost plus published delivery-time cost, with fixed tie-breakers.

The laptop test demonstrates why headline price is insufficient: a $9,000 offer including delivery and a 24-month warranty qualified; a cheaper $8,000 offer excluding both was rejected. A late submission rolled back under the bid deadline. The comparison finalized to bid 0 without making a purchase or transferring supplier funds.

## GenLayer's role
GenLayer is central to eligibility: validators independently fetch hash-pinned quote documents, interpret requirement coverage and price consistency, and agree on normalized conclusions. Permissions, capacity, timestamps, evidence commitments, arithmetic, retry limits and final ranking remain deterministic. Missing or changed evidence cannot automatically qualify.

## Evidence links
- Source: https://github.com/haris4587/QuoteParity
- Intelligent Contract: https://github.com/haris4587/QuoteParity/blob/main/contracts/quote_parity.py
- Deployment: https://explorer-studio.genlayer.com/tx/0x01b62cd94e52506650928cc53a8c64ed66f6a5f064460d070ed4fd70aec332df
- Contract: https://explorer-studio.genlayer.com/address/0x52Bf9E533159ed35Bc473180b1C86908fFD67883
- Scope qualification: https://explorer-studio.genlayer.com/tx/0x7b811ab6fcc72f3c66bbe050dca6a840e05fad11f238ea0384ed967cc500ef91
- Exclusion rejection: https://explorer-studio.genlayer.com/tx/0x0e3441e1ce31ce9ed11690cbf05a1354ce671f45cdd5793eb5b4f3ac531a9ab0
- Final ranking: https://explorer-studio.genlayer.com/tx/0x3bface4d5a2e6f8e16087ad448749fa0a303fafd4205ec6014f206496fb4c242
- Live report: https://github.com/haris4587/QuoteParity/blob/main/docs/live-run.json
- Finalized state: https://github.com/haris4587/QuoteParity/blob/main/docs/finalized-state.json
- Tests and limits: https://github.com/haris4587/QuoteParity/blob/main/docs/VALIDATION.md
- Workflow screenshot: https://github.com/haris4587/QuoteParity/blob/main/docs/studio-proof.jpg
- 512 px PNG logo: https://github.com/haris4587/QuoteParity/blob/main/public/quoteparity-logo.png
- Website: https://quoteparity.itzanza2.chatgpt.site — owner-private until public sharing is explicitly enabled. Do not describe it as publicly reviewable yet.

## Limits to disclose
Studionet development app; synthetic quote fixtures; no escrow or legal purchase award. Supports public UTF-8 text/JSON/static HTML documents up to 32 KB, not PDF uploads or authenticated supplier portals. AI consensus does not establish supplier identity or performance. Repository checks pass; frontend browser visual QA and live funding of a new frontend session account were not completed. The real workflow used the requested Studio built-in wallet.
