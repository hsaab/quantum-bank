# Quantum Bank — demo story (why it is built this way)

This app is a small **Split.io** showcase dressed as a bank. The interesting parts are not the balances; they are **how feature flags interact with real pages, demos, and automated testers**.

## Two lanes on the same product

### Lane A — quick updates (what you show in the room)

You want observers to feel that **the control plane changes the product without a deploy**: flip a treatment in Split, and the **visible experience updates quickly**—ideally without an awkward full reload in the middle of a live demo.

That is **demo mode**: variants can be preloaded (for example via the wrapper + iframe pattern) and the **client-side** Split SDK can react to updates so the link from **flag → UI** is obvious and immediate.

### Lane B — the real site (what testers and most people should traverse)

The same routes and flows should still feel like a **normal product**: one document at a time—home or pricing as a **single** server-chosen variant, then login → dashboard → transfers—**without** parallel hidden trees (no “sneaky” duplicate DOMs from multiple full pages sitting in the page at once).

That is **traditional mode** (default): **server-side** treatment picks **one** template. Refresh to pick up a new treatment if the flag changed.

**In one sentence:** flags can move as fast as the control plane; the surface you test and treat as “the app” stays the canonical, single-variant site.

## Why that matters for AI testers (AIT)

Demo mode’s multi-variant DOM is powerful for spectacle but **hard for agents**: iframes, hidden variants, and inconsistent copy across variants (e.g. “Sign In” vs “Login”) can produce **ambiguous or duplicated** trees. The agent may latch onto the wrong subtree or “fix” the wrong control.

Traditional mode keeps **one** nav, **one** set of labels, and **one** set of `data-testid`s per request—so the story is **flexible tests against a real build**, not wrestling stunt markup.

## How this maps to the code (pointers)

- **Demo vs traditional:** `api/home.py`, `api/pricing.py` (`is_demo_mode`, session `entry_path`, Split `demo_mode`, env `DEMO_MODE`, forced `/demo` route in `app.py`).
- **Variant selection:** Split `home_page_variant` (server in traditional mode; client in demo wrappers)—see [SPLITIO_SETUP.md](SPLITIO_SETUP.md).
- **Deployment:** [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md).

---

## Database — what we use today

| Piece | Reality |
|--------|--------|
| **Engine** | **SQLite** (`sqlite3` in the stdlib). |
| **File** | `quantum_bank.db` in the app working directory (`DATABASE` in `models.py`). |
| **Schema / migrations** | **None in repo**—tables are created in `init_db()` with `CREATE TABLE IF NOT EXISTS`; seed data runs when `users` is empty. |
| **“DB DevOps”** | **Nada** today—no Alembic/Flyway/Liquibase, no managed Postgres wiring in this codebase. |

On **Render free tier**, that SQLite file is **ephemeral** (resets on sleep, deploy, restart)—fine for demos; not durable production. See `RENDER_DEPLOYMENT.md` for persistence options if you outgrow that.

### Roadmap idea (your next chapter)

To **show a feature that requires a real schema change** and a believable **database + DevOps** story, you would typically:

1. **Pick a managed database** (e.g. PostgreSQL on Render, Supabase, Neon, RDS) and point the app at a `DATABASE_URL` instead of a local file.
2. **Introduce migrations** (e.g. Alembic for Flask/SQLAlchemy, or raw SQL migration folders applied in CI/deploy)—so “DB change” is a reviewed artifact, not only `init_db()` edits.
3. **Wire deploy pipeline** so migrations run before or with the new app version (and rollbacks are considered).

Today the app is **intentionally minimal**: SQLite + inline init. That is enough for flag demos and fake banking data; it is the **starting line** for a DB-backed feature narrative, not the finish line.
