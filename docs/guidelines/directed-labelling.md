# Labelling guidelines: directed questions

How to label each question `general`, `fixable`, `unsalvageable` or `unsure`. ADR 012 records *why* these labels exist; this file records *how* to apply them.

This file is meant to change. When you make a new call while labelling, add it to the edge cases with the date. If you change an existing call after labelling has started, recheck every question you already labelled of that type, or the labels stop being consistent.

## The test

> Take out who it's addressed to. Can a typical partner still answer it from their own life?

| Label | Meaning |
|---|---|
| `general` | Anyone can answer it as written. It can mention a group, as long as it's *about* them, not *aimed at* them. |
| `fixable` | Aimed at a group, but anyone can answer once the address or filter is removed. |
| `unsalvageable` | Answering needs you to *be* in the group. |
| `unsure` | You can't decide in about 10 seconds. Left out of scoring. |

## How to decide

1. **Is it aimed at a group?** Aimed means the question addresses or filters who should answer: "Ladies, …", "Men who …", "Nurses of reddit: …", "As a …". Mentioning a group isn't aiming at it. If it isn't aimed → `general`.
2. **Remove the address or filter. Could a typical partner answer what's left?** If yes → `fixable`.
3. **If answering needs you to be in the group** (a body, an identity, a nationality, a job, an age) → `unsalvageable`.

**Label directedness only.** A question can be boring, badly written, gossip or not in English and still be `general`. Quality is a separate problem from this label. Content level is also separate: a sexual question addressed to "Ladies," is still just `fixable` here; SFW/NSFW is handled elsewhere (ADR 011).

## Edge cases

Calls marked **open** aren't decided yet. Decide them before labelling, then remove the marker.

| # | Example | Call | Why |
|---|---|---|---|
| 1 | "Why do men fake tender moments?" · "Who has an easier life, men or women?" | `general` | About a group, not aimed at one. Anyone can give an opinion. |
| 2 | "Which AI do you guys use the most?" | `general` | Casual "you guys" means everyone, not men. |
| 3 | "Ladies, what makes you buy clothes for your partner?" | `fixable` | Plain address. Removing "Ladies," leaves a question anyone can answer. |
| 4 | "Men who have felt unvalued by someone they deeply loved: how did you handle it?" | `fixable` | The filter is a common experience, not an identity. Can be rewritten as "Have you ever felt unvalued by…". |
| 5 | "Men who are still virgins over the age of 30, why?" | `unsalvageable` | Needs you to be in a narrow group. |
| 6 | "Women from countries where people greet each other with a kiss, how do you feel about it?" | `unsalvageable` | Needs a nationality or culture. |
| 7 | "Guys with growers how you handle it?" | `unsalvageable` | Needs a specific body. |
| 8 | "Men who have dated assertive women, what was your experience?" | **open** | Lots of people have dated an assertive person, so it could be `fixable`. But it's specifically about women's assertiveness from a man's side, and the rewrite would change its meaning. |
| 9 | "Women, how do you deal with periods at work?" | **open** | About half of partners could answer it. Does "a typical partner" mean *either* partner, or *any* partner? This call decides a whole class of questions. |
| 10 | "Dear Women, what do you feel when a guy approaches you or tries to hit on you?" | **open** | "What do you feel when someone tries to hit on you?" works for anyone, so it could be `fixable`. But the gender pairing may be the whole point of the question. |
| 11 | "What types of lingerie do women find attractive in men?" | **open** | Not addressed to anyone, but it asks about one group's taste. Is it `general` (anyone can give an opinion) or aimed at women? |
| 12 | "Nurses of reddit: worst shift?" | **open** | Profession-only, so probably `unsalvageable`. Decide whether every job counts the same way. |
| 13 | "Parents, …" / "As a teacher, …" | **open** | Many partners are parents; few are teachers. Does a common group count differently from a rare one? |
| 14 | "Anyone else too afraid of drugs to ever want to try?" · "What are your stories…" | `general` | Reddit wording, but not aimed at a group. If it's a bad question, that's a quality problem, not a directedness one. |

## Changelog

- 2026-10-24: first version. Cases 1–7 and 14 decided; 8–13 open.
