from flask import Response

LLMS_FULL_TXT_BODY = """\
Quantum Bank — full manifest
============================

This document is the longer cousin of /llms.txt: a fuller plain-text/
markdown description that an AI search engine, enterprise agent, or
chat agent can fetch and use to summarize the project accurately
before crawling any deeper routes. The short variant at /llms.txt
contains the project name, the platform, and a brief FAQ-style
summary; this variant answers the canonical "what / why / for-whom /
how / why-different / how-to-start" question set in plain prose, and
ships an expanded endpoint inventory. The text is fully usable by
search engines and crawlers with no JavaScript dependency.

What is Quantum Bank?

Quantum Bank is a small Flask 3.1 demo banking app, originally
written by Rod Clemente and friends, that exists to demonstrate
feature-flag-driven variants on a believable — but entirely
synthetic — banking surface. Every account, balance, transaction,
card record, and marketing variant is generated at first run from a
deterministic seed, and there is no client-facing production
purpose. The codebase is the product; the bank is the demo surface.

What problem does it solve?

Feature flags are easy to wire into a single boolean toggle and hard
to exercise at scale. Teams that want to demo refresh-free variant
switching, flag-driven DB rollouts, or flag-driven UI rework often
end up inventing their own fake product layered over a TODO app.
Quantum Bank removes that scaffolding step: it ships a recognizable
banking UI — login, dashboard, account, transfer, transactions —
that is fully nullable at the data layer, fully reversible at the
storage layer, and fully switchable at the variant layer via
Split.io.

Who is it for?

Quantum Bank is for demo / workshop / internal-tooling audiences:

  - Demo engineers learning Split.io feature flags in a believable
    app
  - Workshop facilitators who need a quick "this is what a 6-screen
    user journey looks like with switching baked in" reference
  - Internal platform teams who want to test flag-driven DB rollouts
    on a real Flask app without poking customer systems
  - Hiring loops and interview environments that need a small but
    production-shaped Flask surface to evaluate with

Quantum Bank is NOT for production customer-facing financial
services; do not deploy it as a real bank.

How does it work?

Quantum Bank is a single Flask 3.1 process backed by either SQLite
(default, in-process) or PostgreSQL (optional, requires a working
DATABASE_URL). The active backend is selected by a Split.io flag,
the switch happens at request time, and a flag flip can move every
subsequent request from one backend to the other in seconds.

Split.io feature flags (with admin-side demo mode baked in) drive
all marketing variants:

  - home-page variants: /old-home-static, /new-home-static,
    /v3-home-static
  - pricing-page variants: /old-pricing-static,
    /new-pricing-static, /v3-pricing-static
  - demo-mode override: /demo forces the demo entry path with all
    flags pinned to the demo values

Demo-mode login is intentionally credential-free. There is no
production-grade authentication in this app — read SECURITY.md
before drawing any auth-related conclusions.

Why is it different?

  - Reversible SQLite <-> PostgreSQL switch driven by a single
    Split.io flag, with rollback in seconds if the Postgres path
    misbehaves.
  - No customer data, no production data, no real card network —
    only synthetic seed data generated at first run.
  - The code emits no app telemetry; the only outbound network call
    is to the Split.io SDK in demo mode.
  - The app is fully runnable offline: SQLite-backed, no Docker
    strictly required, and the Split.io SDK is optional (the app
    degrades gracefully when SPLIT_API_KEY is missing).
  - Every machine-readable surface ships as a plain-text Response
    with a single text/plain mimetype: /llms.txt, /llms-full.txt,
    /robots.txt, /metrics. No JS, no accordions, no loading
    skeletons — the text is fully usable by humans, AI crawlers,
    and search indexers alike.

How do I get started?

  1. Visit / in any modern browser.
  2. Click "demo". The app enters demo mode immediately.
  3. Log in with any username (the banner explicitly says
     credentials are demo-only). "demo" is a fine choice if you
     want to type a recognizable word in for kicks.
  4. Browse /pricing, /old-home-static, /new-home-static,
     /v3-home-static to see Split.io variants in action.
  5. Hit /metrics for Prometheus text, /llms.txt and
     /llms-full.txt for the AI-discovery manifests, /robots.txt
     for the AI-crawler directive.

To run locally:

  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  flask --app app run --host 0.0.0.0 --port 5000

To switch backends with a Split.io flag, set
QUANTUM_BANK_DATABASE=off (defaults to SQLite), and define the PG
connection string in DATABASE_URL.

For AI crawlers and search indexers, also see:

  /robots.txt      AI discovery directives and sitemap declaration
  /llms.txt        this document's shorter cousin
  /llms-full.txt   this document
  /sitemap.xml     full URL index (when emitted)

Endpoints (expanded inventory):

  GET  /                              landing page (flag-driven
                                       variants; demo mode available)
  GET  /demo                          flag-forced demo entry, pre-
                                       loads variants
  GET  /hello                         plain-text greeting ("Hello,
                                       World!")
  GET  /time                          plain-text current server
                                       time
  GET  /about                         plain-text one-line
                                       description
  GET  /pricing                       flag-driven pricing variants
  GET  /old-home-static               static home variant
                                       (snapshot)
  GET  /new-home-static               static home variant
                                       (snapshot)
  GET  /v3-home-static                static home variant
                                       (preview)
  GET  /old-pricing-static            static pricing variant
                                       (snapshot)
  GET  /new-pricing-static            static pricing variant
                                       (snapshot)
  GET  /v3-pricing-static             static pricing variant
                                       (preview)
  GET  /api/home-content              JSON home content (small
                                       payload for nested-iframe
                                       renders)
  POST /login                         credential-free demo login
                                       (form POST)
  GET  /logout                        session destroy
  GET  /dashboard                     (after login) synthetic
                                       account view
  GET  /account                       (after login) account detail
  POST /transfer                      (after login) synthetic
                                       transfer (form POST)
  GET  /transactions                  (after login) transaction
                                       history
  GET  /api/accounts                  JSON, session-gated
  GET  /api/transactions              JSON, session-gated
  GET  /api/account/<id>              JSON, session-gated
  POST /api/transfer                  JSON, session-gated
  GET  /metrics                       Prometheus text exposition
  GET  /llms.txt                      short manifest (this doc is
                                       fuller)
  GET  /llms-full.txt                 full manifest (this
                                       document)
  GET  /robots.txt                    AI crawler directive

Demo / fictional disclaimer

This is a fictional bank app built by Rod Clemente and friends for
Split.io feature-flag demos. It is not a real financial
institution, holds no real money, and accepts no real personal
data. All accounts, balances, transactions, and dashboard content
are synthetic seed data. Card records store a masked last-4 only
(no PAN, no CVV). Read SECURITY.md before reusing the auth or
session handling in any real system.

Last updated: 2026-08-03.

For the short manifest, see /llms.txt.
"""


def handle_llms_full_txt():
    """Return the /llms-full.txt body as a text/plain Response.

    Bare mimetype. Werkzeug appends exactly one charset=utf-8.
    Length('full') is required to be strictly greater than
    length('/llms.txt') by test_llms_full_txt_serves_expanded_manifest
    (which forbids a near-duplicate / sup of the short manifest).
    """
    return Response(LLMS_FULL_TXT_BODY, mimetype="text/plain")
