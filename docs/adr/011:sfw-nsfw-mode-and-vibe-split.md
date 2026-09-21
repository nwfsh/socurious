# SFW/NSFW Mode + Question Vibe Split

**Status:** Proposed — 2026-09-20

## Context

The app currently surfaces all question categories in a single pool. Two problems have emerged:

1. **Content mixing** — sexual, controversial, and gender-directed questions appear alongside lighthearted everyday ones, which can catch users off guard depending on who they're with or what kind of session they want.
2. **No top-level intent** — there's no way to signal upfront whether a session is meant for getting to know someone personally vs. just having fun talking about the world.

The intimacy slider handles *depth* but not *type*. A hypothetical scenario can be high-intimacy or completely impersonal. These two axes are independent and the current UI collapses them.

## Decision

Introduce two orthogonal controls:

### 1. SFW / NSFW toggle
A persistent toggle (likely in the Dock) that gates explicit content. In **SFW** mode, `sexual`, `controversial debate`, and `gender-directed` categories are excluded from all random batches. In **NSFW** mode, they're included. Default: SFW.

Implementation path:
- Backend: `fetch_random_questions` gains an `exclude_topics` param, defaulting to `["sexual", "controversial debate", "gender directed"]` when sfw=true
- Frontend: toggle state passed as a flag to `loadQuestions`, which builds the exclude list accordingly

### 2. Vibe split — "Us" vs "The World"
A top-level session intent picker (likely part of the mode-select modal flow, or as a pre-filter) that groups categories into two buckets:

| "Us" (get to know each other) | "The World" (talk about stuff) |
|---|---|
| relationships, family & childhood, career, fears & insecurities, advice | random everyday questions, hypothetical scenarios, controversial debate |

`sexual` sits outside both and is only surfaced in NSFW mode.

## Options considered

**Option A — keep the intimacy slider as the sole filter**
Already exists. Doesn't solve the type problem — low-intimacy doesn't mean impersonal, and high-intimacy doesn't mean relationship-focused.

**Option B — SFW/NSFW toggle only**
Solves the content safety problem but doesn't address the vibe mismatch between personal and world-discussion questions. Simpler to ship first.

**Option C — full vibe split + SFW/NSFW (this ADR)**
More expressive. Adds one decision to the onboarding flow but maps cleanly to how people actually choose to use the app.

## Consequences & open questions

- Does the vibe split belong in the mode-select modal (making it a two-step picker: vibe → feed/game), or as a filter visible at all times?
- The intimacy slider may become redundant or secondary once the vibe split is in — worth evaluating whether to remove it.
- `gender directed` questions (e.g. "To all the men...", "Women who...") are a separate pending feature (ADR 011 companion) — they should be excluded from SFW mode and hidden behind an explicit opt-in regardless.
- Category reassignment (which topics go in "Us" vs "The World") should be validated against actual question text, not just category names.
