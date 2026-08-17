# Security Policy

## This is a demonstration application

Quantum Bank is a **demo app** built to showcase Split.io feature flags and a
flag-gated SQLite ↔ PostgreSQL backend switch. It is **not** a real bank and
**not** a reference implementation for security or banking systems.

- **All data is synthetic.** Accounts, balances, transactions, and cards are
  fake and seeded at startup.
- **No real money, no real customers, no real card data.** Card records store a
  masked last-4 only — no PAN, no CVV, no expiry beyond a display string.
- **Auth is intentionally trivial.** Login is username-only (`demo`) with no
  password. The session and login handling are demo conveniences and must not
  be reused in production.
- The default `SECRET_KEY` is a development fallback. Any shared or public
  deployment must set a real, secret `SECRET_KEY`.

## Reporting a vulnerability

Because this is a demonstration project with no real users or data, there is no
formal security response process or SLA.

If you spot something worth fixing — for example a way the demo could leak the
synthetic data store, an unsafe default, or a dependency advisory — please open
a GitHub issue (or a pull request) on
[Roderick-Clemente/quantum-bank](https://github.com/Roderick-Clemente/quantum-bank).
For anything you'd prefer not to disclose publicly, use GitHub's private
**Security advisories** feature on the repository.

## Hardening done

Even as a demo, the app has been through a security pass. Notable fixes:

- **Broken object-level authorization (IDOR) in transfers** — `transfer_money`
  now verifies the source account belongs to the acting user before any debit,
  and both the HTML and JSON transfer routes return `403` on a mismatch. Covered
  by cross-user regression tests on both backends.
- **NaN / non-finite amount injection** — transfer amounts are rejected unless
  finite (`math.isfinite`) at both the route and model layers, closing a path
  that could poison balance arithmetic.
- **Container & orchestration hardening** — the image runs as a non-root user;
  `docker-compose` and the Kubernetes manifests set `no-new-privileges`,
  `read_only` root filesystems, and `allowPrivilegeEscalation: false` /
  `runAsNonRoot: true`.
- **Front-end** — Split.io CDN includes are pinned with Subresource Integrity
  (SRI) hashes, and the client-side content swap enforces a same-origin guard.
- **Safe debug defaults** — Flask debug is off unless explicitly enabled via env,
  and the dev server binds to `127.0.0.1` rather than `0.0.0.0`.

## Scope notes

- Static analysis (Semgrep) and dependency/SCA scanning (OWASP Dependency-Check,
  OSV) run in the CI pipeline — see
  [`.harness/pipelines/rodbank-pipeline-ci-reference.yaml`](.harness/pipelines/rodbank-pipeline-ci-reference.yaml).
  The Semgrep stage gates the build at medium severity.
- Do not deploy this app as a real financial service.
