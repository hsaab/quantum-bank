# CI/CD

CI and CD run on **Harness**. The pipeline builds, lints, tests against *both*
database backends, and runs software-composition-analysis on every build; the
service definition deploys the container to Kubernetes.

## Where it lives

| Concern | File |
|---------|------|
| CI pipeline (reference copy) | [`.harness/pipelines/rodbank-pipeline-ci-reference.yaml`](../.harness/pipelines/rodbank-pipeline-ci-reference.yaml) |
| Deploy service definition | [`.harness/quantumbankbackendsvc.yaml`](../.harness/quantumbankbackendsvc.yaml) |
| K8s manifests + values | [`.harness/kubernetes/`](../.harness/kubernetes/) |
| Container image | [`Dockerfile`](../Dockerfile) |
| Render deploy | [`render.yaml`](../render.yaml), [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) |

> The pipeline YAML is stored `INLINE` in Harness Studio; the file here is a
> reference copy kept in sync so the build is reviewable in the repo.

## The CI stage

The `Build` stage runs on a Harness Cloud Linux runner:

1. **Background `postgres:16`** — a service container the Postgres test lane
   connects to.
2. **Lint** — `ruff check .` and `black --check .` (versions pinned; config in
   [`pyproject.toml`](../pyproject.toml)).
3. **Test (SQLite)** — `POSTGRES_DATABASE=off`, JUnit report `out_sqlite.xml`.
4. **Test (Postgres)** — `DATABASE_URL` + `POSTGRES_DATABASE=on`, waits for the
   background DB, then runs the suite with report `out_postgres.xml`.
5. **SCA** — OWASP Dependency-Check and OSV Scanner in parallel.

### Why a dual-backend test matrix

Some bugs are **Postgres-only**, and a SQLite-only CI run stays green straight
through them. Example: Postgres returns `created_at` as a `datetime` while SQLite
returns a string, so template date handling can pass on SQLite and 500 on
Postgres. Running the suite against both engines catches that drift *before* a
[feature-flag flip](feature-flags.md) exposes it in production.

## The CD path

[`quantumbankbackendsvc.yaml`](../.harness/quantumbankbackendsvc.yaml) defines a
Kubernetes service whose manifests and values are pulled from
[`.harness/kubernetes/`](../.harness/kubernetes/) on `main`. Render is supported
as a simpler target via [`render.yaml`](../render.yaml) + the Gunicorn
[`Dockerfile`](../Dockerfile).
