# Validation

- `npm test`: **21 passing tests** (15 Python contract tests, 6 Node/JSDOM application and receipt tests).
- `npm run build`: successful Vite production build.
- Stable GenLayer SDK schema check: passed in real GenVM.
- Deployed source downloaded through `getContractCode` and compared byte-for-byte with `contracts/quote_parity.py`: exact match.
- RPC CORS preflight from the deployed app origin: HTTP 200, explicitly allows the app origin and JSON POST requests.
- Live deployment and purchasing workflow: real full-consensus transactions from Studio's built-in account. Individual receipts and finalized-state snapshot are checked in.
- Initial timestamp accessor error was found in the first live attempt, corrected to `gl.message_raw['datetime']`, and deployed as a fresh instance. Original failed creation/submission receipts are retained. They are not counted as successful live transactions.
- Budget quote's excluded delivery/warranty was rejected by independent validator AI review. Atlas's complete quote qualified. Meridian's submission after the committed deadline was rejected before evidence processing.
- Browser screenshot evidence concerns the real Studio workflow. App visual browser QA was unavailable because the managed preview browser skill was not exposed. JSDOM checks cover rendered content and actions, not responsive pixel layout.
- Frontend session-account funding was not executed as a live agent test: automatic approval review rejected funding a newly generated account because the user required Studio's built-in wallet. The authorized live run uses the funded Studio built-in address. Frontend session-wallet calls are tested with a stubbed client; cross-origin RPC access is independently verified read-only.

This is development-network evidence, not an audit, production readiness certification, legal procurement award, or proof of supplier authenticity. Quote fixtures are fictional and explicitly labelled.
