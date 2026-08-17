from flask import Response

LLMS_TXT_BODY = """\
Quantum Bank
============

Demo disclaimer: this is a fictional bank app built for Rod Clemente &
friends' feature-flag demos (powered by Split.io). It is not a real
financial institution, holds no real money, and accepts no real
personal data. All accounts, transactions, balances, and dashboard
content are synthetic seed data generated at first run.

What this app is
- A Flask 3.1 demo banking app that showcases Split.io feature flags
- A reversible SQLite <-> PostgreSQL backend switch driven by a flag,
  with rollback in seconds if the Postgres path misbehaves
- A login + dashboard + transfer flow, all backed by synthetic data
- Front-end and back-end demos for refresh-free Split.io variant
  switching in demo mode

Useful endpoints
- /            landing page (flag-driven variants; demo mode available)
- /demo        flag-forced demo entry, pre-loads variants
- /hello       plain-text greeting ("Hello, World!")
- /time        plain-text current server time
- /about       plain-text one-line description
- /pricing     flag-driven pricing variants
- /login       credential-free demo login (form POST)
- /dashboard   (after login) synthetic account view
- /account     (after login) account detail
- /transfer    (after login) synthetic transfer (form POST)
- /transactions (after login) transaction history
- /api/accounts, /api/transactions, /api/account/<id>  JSON, session-gated
- /metrics     Prometheus text exposition (text/plain; version=0.0.4)
- /llms.txt    this file (text/plain; charset=utf-8)

What this app is NOT
- Not a real bank. There is no real money, no real customer data, no
  real card network. Card records store a masked last-4 only (no PAN,
  no CVV). Do not reuse the auth or session handling in production.
- Not a security reference. The login flow is a demo flow. Read
  SECURITY.md before drawing any conclusions from this codebase.
- Not a stable public-facing surface. Routes, splits, and the demo
  entries are subject to change without notice.
"""


def handle_llms_txt():
    """Return the /llms.txt body as a text/plain Response.

    Mirrors the /metrics precedent in app.py: wrap the body in a
    Response with an explicit mimetype, rather than returning a
    bare string (which Flask would otherwise default to text/html).
    """
    return Response(LLMS_TXT_BODY, mimetype="text/plain")
