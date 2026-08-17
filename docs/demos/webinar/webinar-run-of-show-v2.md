# Webinar Script v2 — "Zero Downtime, Full Control: Feature Flags for the Modern DBA"

Rebuilt from the **live dry-run with Aaron** — this is *your* delivered flow, tightened, with the real experiment baked in as the climax. ~10 min · DZone, skews DBA · recorded + reused.

**One idea:** FME decouples release from deploy ~90% of the time. The honest exception is when the feature can't run until the schema exists — and that coupled case is where you keep zero downtime *and* hand a human a real, data-driven choice instead of a blind rollback.

**The two-failure spine (don't let them feel redundant — this contrast IS the talk):**
- **Failure #1 (standard pipeline):** fully automatic, no human, self-heals — *because the DB and feature were decoupled.*
- **Failure #2 (coupled pipeline):** AI verify flags it, but then a **human + the experiment** make a targeted business decision — *because here they're coupled and a blunt rollback isn't the only move.*

Read top-to-bottom. **Bold** = say it. *(beat)* = pause. Cut-priority + the refresh wart + cheat sheet at the bottom.

---

## ① Open — over the standard pipeline · 0:00

**Scene:** standard end-to-end pipeline already on screen. DB stages left, flag/rollout stages at the end. Talk from second one — product marketing just handed off "what is feature management," so you're picking up the baton.
**Show:** sweep across the whole pipeline on "most of the time."

> "So here's the deal. Obviously the biggest reason you buy into feature management is to **cut the cord** — your release stops being chained to your deploy. You ship the code dark, you flip it on when you're good, and the database never needs to be part of that critical path. And look — that's true. **Most of the time.** But what happens when the feature *can't* run until the schema's been updated, or the new table's there? *(beat)* So today isn't 'flags decouple everything' — it's: **when that coupling is unavoidable, how do you keep zero downtime and full control anyway?**"

*("Most of the time." = hard stop. Hit "can't.")*

---

## ② Ground them — the standard, 90% of releases · 0:45

**Scene:** same pipeline.
**Show:** gesture across the DB stages (dev → QA → prod), then over to the feature/flag stages at the end.

> "To ground you — this is our standard end-to-end pipeline, and for the **majority** of our releases they go through this automatically. It handles both halves of a release. The **database changes** — you can see we update it in dev, QA, production. And then the **feature release** — there's a human in the loop, we turn it on for QA, for beta, an approval, the GA rollout, we run experiments, and finally we clean up the flag.
>
> And the key thing — this is all happening automatically and **asynchronously.** For 80, 90% of our flags, the DB and the feature flag ride their own tracks. And for most of our code that's not a problem — in fact, **that decoupling is working exactly the way you wanted.**"

---

## ③ Failure #1 — fully automatic self-heal · 1:20

**Scene:** the bank, a release that went bad. Play the discovery, don't narrate it.
**Show:** land on the degraded release → "what's this?" → CV graphs (response time, errors/min, all unhealthy) → rollback steps already done → then the **global DB map**.

> "But it's not always clean. Here's Quantum Bank — we tried to ship a release and there were issues. Degradation of service for some people. So we look here and — *(beat)* man, what's this? *(beat)* Yeah. Failed release. We updated the database as expected, but our **AI verify** caught that something was wrong — we link this into our observability tools — average response time, errors per minute, all unhealthy. *(beat, relief)* So — nothing to worry about. **We're not paging anyone in the middle of the night.** Canary delete, undo the database changes, update the ticket. People come in and fix it first thing tomorrow. It **self-healed.**"

**Show:** global DB map across regions.
> "And we can see this across many databases, many environments, worldwide. While it looked healthy in our US and lower environments, **production in Europe, Middle East, APJ, and Africa came back unhealthy** — so we did the right thing and rolled it all back. Everything's in a good place.
>
> *(the contrast — say it)* So that's standard — 90% of the time, that's all you need. And notice: **no human touched that. It self-healed because the DB and the feature were never tied together.**"

---

## ④ Pivot + the coupled feature — the table moment · 2:15

**Scene:** stay on the bank / move toward the rewards feature. This is the hinge — your real transition was smooth, keep it.
**Show:** hold a finger on "another column?"; slow down hard on "its own table."

> "But this next one's a slightly more complex feature. Quantum Bank's for developers, and we're rolling out a new **rewards program** — built to push people onto our higher **silver and gold tiers.** So this is very important to the business. And the rewards behave completely differently by tier.
>
> So there was a debate back and forth: can we just do this as **another column** on accounts? And because of the complexity, and how much the business is leaning in — we said no. Rewards gets its **own table.** *(beat)* **And the moment it became a new table, the feature and the schema became tightly coupled.** The feature flat-out can't run until that table's there. *(beat)* So we use a different pipeline for when it's coupled like this."

---

## ⑤ The coupled pipeline + the two templates · 3:00

**Scene:** Quantum Bank coupled pipeline in Harness.
**Show:** walk preview → approve → apply in dev; open the **FM template** (point at the alerts listener); open the **DB template** (preview-approve-apply).

> "Here's the pipeline — a little simpler than the standard one, but same DNA. We build in dev. We **preview** the change, our CAB team always wants an approval in the loop — in dev that auto-approves — we **apply** it, then we update the flags using our standard templated way.
>
> And because it's standardized, I pulled it into a template for QA and prod. Here's the **feature-management template** — and notice it leaks into this **alerts listener**, which connects this to our experimentation data. *(plant it)* **You'll see why that matters in a minute.** And here's the **database template** — that same preview, approve, apply."

---

## ⑥ QA — blue-green + the rollback choice · 3:45

**Scene:** QA stage of the coupled pipeline.
**Show:** point at blue-green, the DB update, the flag update, AI verify, the swap, then the rollback branch.

> "In QA we've done a **blue-green.** We update the database, update the flags, run AI verify. Healthy? We swap primary and secondary. And here's the **rollback** — if we roll back, we undo those changes the same way."

### 🎯 OPTIONAL planted Q&A — conditional rollback (only if running ahead)
**Cue:** right after "undo those changes." Pause ~2s for Aaron. If silent, ask it yourself.
> **Aaron:** "Do you always roll back the DB and kill the flag at the same time?"
> **You:** "No — absolutely not. Here we chose to. But if you coded the feature to be **backwards-compatible**, you make the DB rollback **conditional on a tag** the dev adds — then on failure you **auto-kill the flag but leave the schema in place.** Users instantly drop to the safe experience, but the table's still there so **dev and QA keep testing** — no degraded customer experience. Rolling back together is the safe default; decoupling the rollback is the power move once your code can handle it."

*(This beat is now CUTTABLE — you ran long in the dry-run. Keep only if pacing allows.)*

---

## ⑦ Prod — the experiment IS the climax · 4:30

**Scene:** prod canary stage. This is the real centerpiece Aaron built — give it room. Switch to the **Quantum six** project / experiment view.
**Show:** canary deploy, DB update, flag update, AI verify → errors ~30% → **open the errors metric, scroll to bottom, change dimension `overall` → `device`.**

> "In production it's a **canary.** We update the database the same standard way, update the flags, and run AI verify. *(open the result)* And here we can see the errors that came through — about **30%.** And while that looks really unhealthy *(beat)* — we've got more detail."

**Show:** flip the dimension to **device.** iOS reads clean; the rest spike.
> "If we segregate this **by device** — *(beat)* look at that. **iOS has basically no issue.** So the problem's localized — Firefox, Edge, maybe that Chromium browser. *(beat)* In this case we decided to just shut the feature off completely. **But now you have a choice.** If iOS looks healthy, maybe we **target it at iOS users only**, and roll it out to the rest once the devs fix it. **That's a business decision now, not a fire drill.**"

**Show (Aaron's best note — close the loop on rewards):** flip to the rewards/business metric.
> "And because this is a **rewards** feature, the metric that actually matters isn't just errors — it's the business. *(beat)* Did it push people to **sign up** for silver and gold? Did they **buy rewards points?** That's what we're really experimenting on. So the call becomes: we've gathered enough — **let's pull this in, harden it, and ship it right.** *(this is the payoff to the 'you'll see why' plant in ⑤.)*"

---

## ⑧ CODA — migration as a dial (TIME-PERMITTING) · 7:30

**Scene:** FME flag list — `postgres_database` treatments. TOLD, not demoed. **First thing to cut if over time.**

> "One more — and this is the bigger story this unlocks. We recently switched this app from **SQLite to Postgres.** And we didn't make it a cliff — we made it a **dial**, because we had to be sure the data stayed consistent before and after.
>
> *(count them off)* **Off** — old SQLite. Then **old-and-confirmed** — SQLite's still primary, but we **mirror every write to both**, and confirm they match. A week or two of confidence, we move to **new-and-confirmed** — now **Postgres is primary**, still writing to both, still confirming. A month of transactionally-identical parity, and we flip to **Postgres only** and retire SQLite. **Every step's a flag. Every step's reversible. A migration as a dial, not a cliff.**"

---

## ⑨ Live app — show it's real · 8:30

**Scene:** the running app. The rewards flag is **already ON** — don't flip it cold on stage.
**Show:** the dashboard with rewards/transactions visible.

> "And this is all real — the flag's on right now. Here are the transactions, and *(scroll)* there's the rewards. Same app, no redeploy."

> ⚠️ **THE REFRESH WART (read the bottom note).** The schema-off / "killed" state needs a manual page refresh — the front end doesn't live-repaint. **Do not flip the kill live and wait for it to update — it won't, and you'll fumble it like the dry-run.** Either pre-stage the off-state in a second tab and cut to it, or just *say* "here's what it looks like when the schema's not there" over a screenshot. Don't gamble it on the recording.

---

## ⑩ Close — better together + CTA · 9:15

> "So here's the punchline. FME does **experimentation and targeting** really well. DB DevOps does **database changes** really well. Put them together and you stop just *shipping* schema changes — you **experiment** on them. Flag the transaction time, the errors, the rewards signups — measure the real-world impact, before and after — and if it's not better, kill it or target it with a flag, instantly.
>
> Because the changes that bite you usually don't show up in the tests. They show up when a million people hit the site. *(beat)* That's the last mile — and this is how you cross it safely. That's zero downtime, full control, for the modern DBA. `[CTA]` — come talk to us if this is the thing you've been fighting."

---

# Production notes

## Cut-priority (you ran long in the dry-run — Aaron: "you went through a lot")
Cut top-down until you fit 10 min:
1. **⑧ the dial** — first to go. It's a told story, not a demo; the experiment is the better climax.
2. **⑥ planted Q&A** — keep only if pacing's comfortable.
3. **③ global map** — compress to one sentence if tight.
4. Protect at all costs: **③ self-heal**, **④ table moment**, **⑦ the experiment.** Those three are the talk.

## The refresh wart (the one real live-failure risk)
Front end doesn't dynamically repaint, so the kill/legacy state needs a manual refresh ([rewards-rollout.md:37](rewards-rollout.md#L37) restart rule + per-request reads). On a recording, **never flip-and-wait.** Options, best first:
- **Pre-stage** the off/legacy state in a second browser tab; cut to it when you want to show it.
- **Screenshot** the legacy banner; narrate over it.
- If you must do it live, **refresh deliberately and say so** ("let me refresh — this is running locally") so it reads as intentional, not broken.

## Honesty framing (it's local; never say "fake")
You handled this fine live. If asked: "this is running locally — the application code and the flag logic are real; the cloud pipeline is our reference architecture for the pattern." True, clean.

## What's real now vs. the script's earlier assumptions
- **REAL & demoable:** the experiment with the **device dimension** (Aaron built it in the **Quantum six** project — iOS clean, others spiking), the coupled pipeline + templates, the rewards feature on SQLite, the flag resolution ([db_flags.py:75](../../db_flags.py#L75)), the savepoint money-safety ([models.py:776-791](../../models.py#L776-L791)).
- **Add for reuse (Aaron's note):** rewards **business metrics** in the experiment (signups, points purchased), not just errors-by-device — it closes the loop back to "why we built rewards."
- **TOLD, not built:** the dial's mirror-write states; the live kill needs the refresh fix.

## Stage cheat sheet
- Transfers must be **$10+** or no points fire ([rewards-rollout.md:100](rewards-rollout.md#L100)).
- Experiment lives in project **Quantum six** → errors metric → scroll to bottom → **dimension: overall → device.**
- Fresh Chrome profile for the live app so nothing leaks into the demo.
- Keep the log tail (`rewards.rollout.*`) visible during the live app beat — your receipts.
