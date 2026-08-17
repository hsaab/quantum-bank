# Webinar Re-Record Plan — patch segments for the polished MP4

**Why this doc:** DZone is sending a first-draft MP4 and offered to **freeze/extend your frame** over dead spots and let you **re-record screen shares on your own time** to splice in. This is the shot list for those inserts.

**Context (from the live run):** the talk landed well — audience liked it, felt smooth. The only real defect was the **screen-share dropping ~4 times**, twice mid-content. There was **no on-screen notification** to you when it dropped (you only caught it from the stage monitor), which is why it recurred. So: re-records are screen-only inserts; your live audio/narration was fine and mostly reusable.

---

## Decision gates (do these first)

1. **Wait for DZone's first-draft MP4.** Don't re-record blind — see exactly which seconds are dead and how much they can freeze-frame vs. need a true insert. Their words: "we'll send the first draft over and you tell us which pieces are best to re-record."
2. **Match the live setup so inserts are seamless:** same browser/profile, same Harness project, same zoom level, same window chrome, same theme. A mismatched UI is more jarring than a freeze-frame.
3. **Record screen-only, narrate to match your live audio cadence.** If the editor keeps your live VO and just swaps the visual, you only need clean cursor movement timed to what you already said. If they want fresh audio, re-read from the v3 lines.
4. **Lock the device story before recording** (see below) — this is the one content inconsistency to fix while you have the chance.

---

## Priority 1 — must re-record (drops hit mid-content)

### Insert A — Coupled pipeline + templates  *(live drop @ transcript line 705)*
**What broke:** you were walking the templatized QA/prod stages and the share dropped mid-sentence ("you can see here that I've…" → cut).
**Why it matters:** this is the proof that the coupled pipeline is real and standardized — the structural payoff of the whole "when coupling is unavoidable" promise. A freeze-frame can't carry it; needs clean screen.
**Shot list (screen-only, ~60-90s):**
1. Coupled pipeline overview — name it as simpler-than-standard, same DNA.
2. Dev stage: **preview → approve → apply** (call out auto-approve in dev).
3. Open the **FM template** — point at the **alerts event listener** (the experimentation-metric ingest). Say the foreshadow line: "I'll show you why that matters in a minute."
4. Open the **DB template** — same preview-approve-apply.
5. **QA = blue-green**, verify, swap; show the predefined rollback (roll back DB + flip flags off).
6. **Prod = canary**, verify against observability + experimentation; show the rollback branch.
**Script:** v3 §⑤.
**Watch:** keep the alerts-listener mention — it's the setup for the experiment climax.

### Insert B — The experiment (the climax)  *(live drop @ transcript line 790)*
**What broke:** share dropped right as you said "you can see here we have the total latency" → cut. This is your **best 60 seconds** and it got truncated live.
**Why it matters:** this is the literal answer to the hook ("full control") and the one-plus-one-equals-five moment. It must be flawless in the cut.
**Shot list (screen-only, ~75-90s):**
1. Open the **rewards rollout experiment.**
2. Show it captures **query-level latency + errors** (full-stack), not just business stats.
3. Drill into **errors** → ~**20-30%** rate.
4. **Change the dimension `overall` → `device`** (the reveal — do it slowly, let it land).
5. **iOS = healthy; Android = the broken segment** (optionally note desktop Chromium/Edge).
6. Land the **business decision:** keep on iOS (largest/highest-paying), kill on Android until fixed.
**Script:** v3 §⑥.
**🔒 LOCK:** say **iOS healthy / Android broken** — identical to Insert A's foreshadow and to any other mention. (Live you wavered between Edge/Chromium/Android — don't.)

---

## Priority 2 — re-record only if the draft shows them damaged

### Insert C — Open + standard pipeline  *(early drops @ lines 623, 650)*
The very start had share-request fumbles before you got going. Your narration was fine; this is likely **freeze-frame / re-share-the-static-pipeline** territory, not a full re-record. Only re-shoot if the draft looks choppy. If you do: v3 §①–§③ (opener → ground-them → failure #1 self-heal + global map). Keep the clean "no human had to jump in — it self-healed because DB and feature weren't tied together" contrast line.

### Insert D — Migration dial coda  *(drop risk @ §⑦)*
Told-not-demoed; lower stakes. Re-record only if it's visibly broken. If you do, **pair it with the honesty exchange** ("we're not doing the migration, we're controlling access / de-risking the release") — that's a credibility line worth having clean. v3 §⑦.

---

## Do NOT re-record (live gold — protect these)
- The **"poor man's feature management system"** anti-pattern laugh.
- The **"did you put your screen sharing behind a feature flag?"** save — it's charming and humanizing; only trim if the editor needs the seconds.
- The **LLM-deleted-my-prod-database / "you told me not to touch it"** bit in the wrap-up.
- Aaron's **"is it really this easy?"** and **conditional-rollback** exchanges — they landed; keep the live takes.

---

## Editor handoff notes (what to tell DZone)
- **Cut:** the 1-min countdown and pre-roll setup chatter (they offered).
- **Freeze/extend:** over the ~4 share-drop gaps until the corresponding insert (A/B at minimum) is spliced.
- **Splice points:** Insert A replaces the dead span starting ~line 705; Insert B replaces ~line 790. I'll provide exact MP4 timestamps once the draft arrives.
- **Audio:** prefer keeping my live VO and swapping only the visual where possible; I'll re-record VO only for segments where the live audio also broke.
- **Lower-third / captions:** if device names appear in captions, ensure they read **iOS / Android**, matching the re-recorded visual.

## Self-record checklist (your own time)
- [ ] First-draft MP4 reviewed; exact dead-segment timestamps noted.
- [ ] Same browser profile / Harness project / zoom / theme as live.
- [ ] Screen-share notification visible this time (second monitor or in-frame indicator) so nothing drops silently.
- [ ] Device story = **iOS healthy / Android broken**, locked.
- [ ] Insert A recorded (pipeline + templates).
- [ ] Insert B recorded (experiment → device dimension → business call).
- [ ] $10+ transfers used if any live-app footage is needed.
- [ ] Files sent to DZone with splice-point timestamps.
