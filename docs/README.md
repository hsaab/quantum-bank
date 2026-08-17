# Documentation

Start with the three capability guides — they map each part of the demo to the
files that implement it. The rest is setup, demo scripts, and reference.

## Capability guides

| Guide | What it covers |
|-------|----------------|
| [feature-flags.md](feature-flags.md) | Harness FME flags: runtime backend switch, rollout flags, live variant switching |
| [db-devops.md](db-devops.md) | Versioned schema, dual-backend data layer, gated/reversible rollout |
| [cicd.md](cicd.md) | Harness CI (lint + dual-backend test matrix + SCA) and CD to Kubernetes/Render |

## Setup

| Doc | What it covers |
|-----|----------------|
| [LOCAL_POSTGRES.md](LOCAL_POSTGRES.md) | Native local Postgres (Homebrew), env, smoke, tests |
| [SPLITIO_SETUP.md](SPLITIO_SETUP.md) | FME/Split keys and flag definitions |
| [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) | Deploy to Render (Docker, env, custom domain) |

## Demos

| Doc | What it covers |
|-----|----------------|
| [demos/rewards-rollout.md](demos/rewards-rollout.md) | Rollout walkthrough: baseline → fallback → ready → forced fail → recovery |
| [demo-fun.md](demo-fun.md) | Why the app is shaped the way it is (demo spectacle vs. realistic site) |
| [demos/webinar/](demos/webinar/) | Webinar run-of-show and recording notes |

## Reference

| Doc | What it covers |
|-----|----------------|
| [TECHSUMMARY.md](TECHSUMMARY.md) | Architecture deep-dive, dual-SDK pattern, demo replay refs |
| [security/SECURITY_REMEDIATION_PLAN.md](security/SECURITY_REMEDIATION_PLAN.md) | Security remediation tracking |
| [screenshots/README.md](screenshots/README.md) | Which pages to capture for the README |
