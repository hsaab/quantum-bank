# Webinar Script v3 — "Zero Downtime, Full Control: Feature Flags for the Modern DBA"

**Canonical / as-delivered.** Built from the live webinar transcript (with Aaron Newcombe) — these are the lines that actually worked on air, tightened. This is the record-of-truth for reuse (DZone recording → Wells Fargo, DB DevOps workshop) and the base for any re-record.

~30 min slot incl. intro + Q&A; the live demo runs ~16 min. Two presenters: **Aaron** (host, FME) sets up + asks; **Rod** drives the demo.

**One idea:** FME decouples release from deploy ~80-90% of the time. The honest exception is when the feature can't run until the schema exists — and *that* coupled case is where you keep zero downtime *and* hand a human a real, data-driven choice instead of a blind rollback.

**The two-failure spine (the whole talk):**
- **Failure #1 (standard pipeline):** fully automatic, no human, self-heals — *because DB and feature were decoupled.*
- **Failure #2 (coupled pipeline):** AI verify flags it, then a **human + the experiment** make a targeted, by-device business decision — *because here they're coupled and a blunt rollback isn't the only move.*

Legend: **Scene** = what's up · **Show** = what you click · `[⚠ DROP]` = screen-share dropped here live, candidate for re-record (see re-record doc) · **bold** = load-bearing.

---

## Pre-demo (Aaron, on slides — keep tight)

Aaron frames it; Rod color-commentates. Reusable lines that landed:
- **The pain:** "database changes are still an all-or-nothing event — big-bang, fingers crossed, no kill switch, and if it goes wrong you're in the war room." (Aaron)
- **The anti-pattern (got a laugh — keep):** "the anti-pattern is trying to use your database as a **poor man's feature management system**, which creates pain for everyone." (Rod)
- **The three use cases:** (1) schema migration / new table — *live demo*, (2) query optimization & index rollouts, (3) database migration. "We'll combine these two superpowers — DB DevOps + feature management & experimentation — into something bigger."
- **CTA to ask early:** "use the live Q&A box now — don't wait till it's almost over."

---

## ① Open — over the standard pipeline · cut to demo

**Scene:** Aaron hands off ("let's cut over to Rod and talk about this zero-downtime schema migration"). Standard end-to-end pipeline on screen. DB stages left, flag/rollout stages at the end.
**Show:** sweep across the whole pipeline on "most of the time."

> "Here's the deal. One of the biggest reasons many of us bought into feature management is to **cut the cord** — your release stops being chained to your deploy. You ship the code dark, you flip it when you're good, and the database doesn't need to be part of the critical path. And that's true — **most of the time.** But what happens when the feature *can't* run until the schema's been updated, until the table's been created? *(beat)* So today isn't about flags decoupling everything — it's: when that coupling is unavoidable, **how do you keep zero downtime and full control?**"

*("Most of the time." = hard stop. Hit "can't.")*

---

## ② Ground them — the standard, 80-90% of releases

**Scene:** same pipeline.
**Show:** gesture across DB stages (dev → QA → prod), then to the feature/flag stages at the end.

> "But before we jump in — to ground you, here's our standard end-to-end pipeline. For the majority of releases, they go through this automatically, and it handles both halves. The **database changes** — you can see we apply updates in dev, QA, production. And the **feature release** — humans in the loop where needed, turn it on for QA, for beta, get an approval, the GA rollout, run experiments, and finally clean up the flag.
>
> And the key thing — this is all happening automatically and **asynchronously.** For 80 to 90% of our releases, the DB and the feature flag ride their own tracks. For most of our code that's not a problem — in fact, **that decoupling is working exactly the way you wanted.**"

---

## ③ Failure #1 — fully automatic self-heal

**Scene:** Quantum Bank — "a bank built for developers, it's fictitious" — watching a live release that went bad. Play the discovery, don't narrate it.
**Show:** land on the degraded release → CV graphs (avg response time, errors/min — all unhealthy) → rollback steps already done (canary delete, DB reverted, ticket updated) → global DB map.

> "If we take a look here — this is Quantum Bank, a bank built for developers. We tried to ship a release and there were some issues — a degradation of service for some people, looks like in some international locations. *(beat)* Okay — this is a **failed release.** We updated the database as expected, but our **AI verify** caught that something was wrong. And the good news is it's all linked to our observability tools, so we can drill into average response time, errors per minute for this transaction group — all really unhealthy, above where we'd want them.
>
> But — no worries. **We're not paging anyone, not waking anyone up in the middle of the night.** It did a canary rollback delete, undid the database changes, and updated the ticket so people can fix it first thing tomorrow. It's **self-healed.**"

**Show:** global DB map.
> "And we can look across all my database environments worldwide. The last few changes were healthy — but this one was healthy for the US, while **production in the Middle East, the EU, APJ, and Africa all came back unhealthy.** So we did the right thing, rolled it back, everything's in a good place."

**THE CONTRAST (the hinge — say it):**
> "So that standard works 90% of the time, and that's all you need. And notice — **no human had to jump in. It self-healed because the database and the feature flag were not tied together.**"

### 🎤 Aaron value-add exchange (keep — it reframes the value)
> **Aaron:** "But there's still a lot of value here, right? You still did that rollback automatically and cleanly — this would've been a nightmare without a tool like this."
> **Rod:** "That's right. One of the key things with Harness — we ask you to define your **happy path** and your **unhappy path** up front. Wire that into your observability tools and we can determine *fast* when unhealthy code ships. We tested extensively in the lower environments — but **you can't simulate production in a box.** There's nothing like real user traffic."

---

## ④ The coupled feature — the table moment

**Scene:** moving toward the rewards feature. Slow down on "its own table."
**Show:** hold a finger on "another column?"; land hard on "its own table."

> "So with this new **rewards** feature we're building — it's a slightly more complex one. It's very important to the business; we want to push people onto our higher **silver and gold tiers**, and the rewards behave very differently by tier. So there was a lot of debate back and forth — *can this just be another column on the account? That'd be a lot less painful.* But because of the complexity and how much the business is leaning in, we said **no — rewards really needs to be its own table.** *(beat)* And that's the moment it became tightly coupled. The feature **cannot run until that table's there.** So we've got a different pipeline for when it's coupled like this."

---

## ⑤ The coupled pipeline + templates `[⚠ DROP — line 705]`

**Scene:** Quantum Bank coupled pipeline in Harness. *(This is where a screen-share drop cut you off live — strong re-record candidate.)*
**Show:** foreshadow the SQLite→Postgres migration (testing both); walk preview → approve → apply in dev; open the **FM template** (point at the alerts event listener); open the **DB template** (preview-approve-apply); QA blue-green; prod canary.

> "I'll foreshadow a little — we recently did a migration from **SQLite to PostgreSQL**, stressed SQLite as far as it'd go. So you'll see we're still testing extensively in **both** environments. Then deploying into dev, it's our standard way: **preview** the change, **approve** it — that approval can be your DBA or change-management users; in dev it auto-approves since we have more control — then run the standard flag release.
>
> Because it's standardized, I pulled it into a **template** for the later environments — so even though each releases a bit differently, we share templates and enforce our standards. In **QA** we don't want to knock the QA team down, so it's **blue-green.** Here's the flag-rollout template — and notice this **alerts event listener**: this one's more sensitive, so we ingest the experimentation metric data. *(I'll show you that in a minute.)* The DB template is the same preview-approve-apply. We verify, then swap blue for green once it's healthy. If it's not, the **rollback's predefined** — roll back the DB change, flip the flags off.
>
> And in **production** it's a **canary** — one of the nice things about Harness is blue-green and canary are easy right out of the box. Update the production DB, update the flags, verify against both observability and experimentation metrics. And here's where we define the rollback: if it's unhealthy, canary delete, undo the DB change, turn the flags off."

### 🎯 Planted Q&A — conditional rollback (Aaron) — KEEP, it landed
**Cue:** right after "turn the flags off."
> **Aaron:** "Do you always want to roll back the database changes *and* kill the flag simultaneously? Or do you do those separately?"
> **Rod:** "In this situation we decided to do both. But I can make the database rollback **conditional** — the dev includes a **tag** that says whether it's required. In this case the flag alone is enough; we don't have to undo the schema. So we give you the flexibility — **it's a choice.** You define what makes sense for your use case."

### 🎤 Aaron "is it really this easy?" (keep — sets up scalability/governance)
> **Aaron:** "You make it look easy — but is it really this easy to put together? How hard would it be without the tool?"
> **Rod:** "It's really straightforward. This is designed to make life easier for the developer — especially in large enterprises where you can't make production changes yourself and have to work across teams. It lets central DevOps teams drive standards. Honestly, **the database is the last frontier for DevOps** — and policies in the product enforce it: no crazy naming schemes, change management codified, so DBAs are comfortable they don't have to be in the critical path babysitting releases."

---

## ⑥ The experiment — the climax `[⚠ DROP — line 790]`

**Scene:** the rewards rollout experiment view. *This is the centerpiece — give it room.* (Aaron built this; it's real. A drop cut you off right at "total latency" live — re-record candidate.)
**Show:** open the **rewards rollout experiment** → query-level latency + errors → drill into **errors** (~20-30%) → **change dimension `overall` → `device`** → iOS clean, Android (+ Chromium/Edge) spiking.

> "Let me show you what that looks like. I've got this **rewards rollout experiment.** And because our feature management is **full-stack**, it captures more than cosmetic or business stats — we can grab **query-level latency and errors** too. And the important part is we can **target** on them.
>
> So if I drill into the errors — *(beat)* we're seeing about a **20-30% error rate.** But if I **segregate by device** — *(beat)* hold on. **iOS is healthy.** The problem's localized to **Android** *(and our desktop Chromium/Edge)*. *(beat)* So now it becomes a **business decision.** I could play it safe and shut it off for everyone. **But** if the business loves the impact on their key metrics — and **iOS is our largest, highest-paying segment** — maybe the answer is: leave it **on for iOS**, **off for Android** until the devs fix the Android code. **Either way, we rolled out safely in production, killed it where it misbehaved, gathered the data — and now we build it right.**"

> 🔒 **DEVICE STORY — LOCK THIS** (you wavered live between Edge/Chromium/Android): canonical version is **iOS = healthy → keep; Android = the broken segment → kill.** Say it identically everywhere. Optional: "desktop Chromium/Edge also affected." Don't contradict it in the re-record.

### 🎤 Aaron — "that's where these two things come together" (keep — names the thesis)
> **Aaron:** "And that's the key — that's where these two things come together. You turn it off for an individual segment — a region, a device, whatever you segment by — and roll back to the old way for just that slice."
> **Rod:** "Exactly — in this case, the old schema. We rolled out safely, contained the blast radius to one segment, and kept the benefit for everyone else."

---

## ⑦ CODA — migration as a dial (time-permitting) `[⚠ DROP risk]`

**Scene:** FME flag list — the migration-control flag. **TOLD, not demoed.** First to cut if over time.

> "One more thing I'll touch on. Remember that SQLite → PostgreSQL migration I foreshadowed — that's why I had testing lined up for **both.** I had a **flag controlling the migration.** Off was the legacy SQLite. But instead of flipping straight on, we needed **trust** that the transactions lined up identically. So we started at **old-and-confirmed** — SQLite is primary, the thing we trust, but we **mirror every write to PostgreSQL** and run a data-integration job to externally confirm they're identical. After a multi-week period, we flip to **new-and-confirmed** — still mirroring, but now **Postgres is primary.** A few more weeks of confidence, and we go **Postgres-only** and retire SQLite. **Every step's a flag. Every step's reversible.**"

### 🎤 Honesty exchange (Aaron) — REUSE VERBATIM, this is the credibility line
> **Aaron:** "One thing — we're not actually *doing* the migration here. It's more like we're controlling the access."
> **Rod:** "Exactly right. We're not doing the migration itself — that's whatever data-integration tool you use. This is at the **application side**: making sure you have **zero downtime** during an inherently risky change like switching databases. **We're helping you de-risk that release.**"

### 🎤 "What databases do you support?" (audience Q — keep the list handy)
> Supported: **Oracle, MS SQL, PostgreSQL, MongoDB, Azure SQL, Azure DB for Postgres.** Roadmap: **YugabyteDB, Teradata, BigQuery.** "All documented in our docs." Plus **warehouse-native experimentation** (Snowflake/BigQuery) — plug experiments straight into your data warehouse, no ETL, so sensitive/governed data never leaves; export results back to the platform.

---

## ⑧ Use case 2 — query optimization (slides, brief)

> "This is what I was alluding to — transaction time. We didn't see it as the culprit here, but the idea: split traffic to a small segment, target specific users, run a 50/50 — say users in Austin or the Middle East — and see how it behaves. Instead of the **highest-paid opinion in the room**, you get **hypothesis-driven development.** Same for AI: you ask the LLM 'how do I improve this query,' but you can't test it without production traffic — so you put it behind a flag. **There's nothing like hitting reality to tell you if it's a good idea or a hallucination.**"

---

## ⑨ Wrap-up + CTA (slides, both)

**Takeaways (Aaron + Rod trade these — they landed):**
- "If you're a DBA / database team / DevOps and you're **not using feature flags** — you should. Instant kill switch, redirect traffic from one query to another, go back to a known-good state without a full rollback."
- "Especially as you get **deluged with AI-driven code changes** — flags save you time and headache."
- **Targeting power (Rod's strong add):** "flags around your logs — turn on high-fidelity debug logging for one segment without blowing out your Splunk bill. Precise control over who sees what."
- **DB DevOps:** "supports **Liquibase and Flyway.** The database is the **last frontier** for DevOps. One plus one equals five when you combine modules. This is **not the time, with AI on board, to do this by hand** — you need orchestration, visibility, governance." (the "LLM deleted my prod database / *you told me not to touch it*" meme bit landed — keep it.)
- **Resources:** the AI-code + feature-flags webinar; the **2026 State of AI-Driven Software Releases** report; "**Infrastructure-as-code isn't enough for databases.**"

**CTA:** "Sign up free, use any module. QR code → a demo of **FME** or **DB DevOps**. Everybody's environment is different — book a demo and we'll tailor it to **your stickiest releases**, rather than just hearing us talk about it."

---

# Production notes

## What was real vs. illustrative (for honest reuse)
- **Real & demoable:** the experiment with the **device dimension** (iOS clean / Android broken), the coupled pipeline + templates, the rewards feature, the flag resolution ([db_flags.py:75](../../../db_flags.py#L75)), the savepoint money-safety ([models.py:776-791](../../../models.py#L776-L791)).
- **Honestly framed live (reuse the Aaron exchange):** "we're not doing the migration, we're controlling access / de-risking the release." Never say "fake."
- **Told, not built:** the dial's mirror-write states; runs locally (GCP/qbank.dev not wired).

## Known issues from the live run
1. **Screen-share dropped ~4×** (lines 623, 650, 705, 790) — twice mid-content (template walk, experiment intro). DZone will re-cut/freeze-frame and let you **re-record screen shares on your own time** → see `webinar-rerecord.md`.
2. **Device story wavered** (Edge/Chromium vs Android) — locked above; fix in re-record.

## Stage cheat sheet
- Transfers must be **$10+** or no points fire ([rewards-rollout.md:100](../rewards-rollout.md#L100)).
- Experiment: errors metric → scroll to bottom → **dimension: overall → device.**
- Live-app kill state needs a **manual refresh** (no live repaint) — narrate it or pre-stage; never flip-and-wait on a recording.
- Fresh Chrome profile so nothing leaks into the demo.
