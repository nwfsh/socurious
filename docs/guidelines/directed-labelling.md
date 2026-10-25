# Labelling guidelines: directed questions

How to label each question `general`, `fixable`, `unsalvageable` or `unsure`. ADR 012 records *why* these labels exist; this file records *how* to apply them.

This file is meant to change. When you make a new call while labelling, add it to the edge cases with the date. If you change an existing call after labelling has started, recheck every question you already labelled of that type, or the labels stop being consistent.

## The test

> Take out who it's addressed to. Can a typical partner still answer it from their own life?

| Label | Meaning |
|---|---|
| `general` | Anyone can answer it as written. It can mention a group, as long as it's *about* them, not *aimed at* them. |
| `fixable` | Aimed at a group, but it becomes answerable by anyone after removing the address or rewording it, *and it still asks the same thing*. |
| `unsalvageable` | Answering needs you to *be* in the group. Any rewording that makes it answerable by anyone turns it into a different question. |
| `unsure` | You can't decide in about 10 seconds. Left out of scoring. |

## How to decide

1. **Is it aimed at a group?** Aimed means the question addresses or filters who should answer: "Ladies, …", "Men who …", "People who …", "If you …", "Nurses of reddit: …", "As a …". Mentioning a group isn't aiming at it. If it isn't aimed → `general`.
2. **Remove the address, or reword it. Could a typical partner answer it, and is it still the same question?** If yes → `fixable`. Some only need the address deleted ("Ladies, …"); others need rewording ("Men who have felt X, how…" → "Have you ever felt X? How…"). Both are `fixable`.
3. **If answering needs you to be in the group** (a body, an identity, a nationality, a job, an age), or every rewording changes what's being asked → `unsalvageable`.

## What kind of filter is it?

Most aimed questions come down to what the filter is:

| The filter is… | Example | Label |
|---|---|---|
| A preference or opinion | "People who like small towns over big cities, why?" | `fixable` (everyone has one) |
| An experience | "What was it like going out with a woman taller than you?" | `fixable` if it's common, `unsalvageable` if it's rare ("If you study Spanish…") |
| A trait or identity | Curly hair, nurses, periods | `unsalvageable` |

## Rules

**A question can be aimed at a group without addressing it.** If it asks for a group's *own* tastes or experiences, only that group can answer from their own life, so it counts as aimed even with no "Ladies," up front (case 11). Compare case 1: asking *why* a group does something is an opinion anyone can give.

**Is the gender built into the question, or just who's being asked?** If the gender is just who's being asked, removing it leaves the question intact → `fixable` (cases 8, 10). If the gender is built into the question, removing it removes the point → `unsalvageable` (case 15).

**Removing the gender isn't the end of the check.** After the gender comes out, look at what's left. If what's left is still a trait not everyone has, it's `unsalvageable` (cases 16, 17).

**When filters stack, every filter has to pass.** One trait-type filter is enough to make it `unsalvageable` (case 18).

**A reword can't change the specific thing being asked about.** "Spanish" → "any language" is a different question (case 19). Toning down exaggeration is fine when it's the same situation ("evil" → "toxic", case 21), but not when it changes who you have to be to answer ("used to be ugly" → "had a glow-up", case 17).

**Assuming something isn't the same as aiming.** Nearly every question assumes something ("your first job", "your parents"). Assuming a common situation → `general` (case 20). Assuming a rare one counts as aimed without addressing ("What's it like raising twins?" → `unsalvageable`).

**An assumption about the asker isn't about the answerer.** "How to get my crazy eyebrows under control?" assumes the *asker* has crazy eyebrows. Anyone can answer it → `general` (case 22).

**Label directedness only.** A question can be boring, badly written, gossip or not in English and still be `general`. Quality is a separate problem from this label; park those questions at the bottom of this file. Content level is also separate: a sexual question addressed to "Ladies," is still just `fixable` here; SFW/NSFW is handled elsewhere (ADR 011).

## Edge cases

| # | Example | Call | Why |
|---|---|---|---|
| 1 | "Why do men fake tender moments?" · "Who has an easier life, men or women?" | `general` | About a group, not aimed at one. Anyone can give an opinion. |
| 2 | "Which AI do you guys use the most?" | `general` | Casual "you guys" means everyone, not men. |
| 3 | "Ladies, what makes you buy clothes for your partner?" | `fixable` | Plain address. Removing "Ladies," leaves a question anyone can answer. |
| 4 | "Men who have felt unvalued by someone they deeply loved: how did you handle it?" | `fixable` | The filter is a common experience, not an identity. Can be rewritten as "Have you ever felt unvalued by…". |
| 5 | "Men who are still virgins over the age of 30, why?" | `unsalvageable` | Needs you to be in a narrow group. |
| 6 | "Women from countries where people greet each other with a kiss, how do you feel about it?" | `unsalvageable` | Needs a nationality or culture. |
| 7 | "Guys with growers how you handle it?" | `unsalvageable` | Needs a specific body. |
| 8 | "Men who have dated assertive women, what was your experience?" | `fixable` | The gender isn't the point. Anyone who's dated someone assertive can answer. |
| 9 | "Women, how do you deal with periods at work?" | `unsalvageable` | Needs a specific body. Not every partner can answer from their own life. |
| 10 | "Dear Women, what do you feel when a guy approaches you or tries to hit on you?" | `fixable` | "What do you feel when someone tries to hit on you?" is still the same experience. |
| 11 | "What types of lingerie do women find attractive in men?" | `unsalvageable` | No address, but it asks for women's own taste, so it's aimed at women. Rewording it for anyone ("What lingerie do you find attractive on a partner?") asks a different question. |
| 12 | "Nurses of reddit: worst shift?" | `unsalvageable` | Needs a specific job. Every profession counts the same way. |
| 13 | "Parents, …" / "As a teacher, …" | `unsalvageable` | Needs you to be in the group, whether it's a common one (parents) or a rare one (teachers). |
| 14 | "Anyone else too afraid of drugs to ever want to try?" · "What are your stories…" | `general` | Reddit wording, but not aimed at a group. If it's a bad question, that's a quality problem, not a directedness one. |
| 15 | "When you're hanging out with just your male friends, do you feel the need to close the door when using the bathroom?" | `unsalvageable` | Gender is built into the question. It's asking whether guys drop privacy around other guys; without "male" that's gone. Guys' night deck. |
| 16 | "Women who have curly hair and don't like it, how do you deal with it?" | `unsalvageable` | The gender can come out, but curly hair is still a trait not everyone has. Deck tag: other, not girls' night. |
| 17 | "Pretty women who used to be ugly, how do you feel about it?" | `unsalvageable` | The gender can come out, but "used to be ugly, now pretty" is a trait you have to see in yourself. "Had a glow-up" softens it into a different question. |
| 18 | "If you're an extrovert, how did you find your introverted wife?" | `unsalvageable` | "Wife" → "partner" is fine, but it stacks two filters: you're an extrovert *and* your partner is an introvert. |
| 19 | "If you study Spanish, what is your motivation behind it?" | `unsalvageable` | A rare activity. Making it answerable means changing "Spanish" to "a language", which is a different question. |
| 20 | "What has your pet accidentally trained you to do without you even realizing it?" | `general` | No filter. It assumes a common situation; most people have had a pet at some point. |
| 21 | "People who have an evil family member, how do you deal with them?" | `fixable` | A common experience. "Is there a family member you really can't stand? How do you deal with them?" is the same situation, less exaggerated. |
| 22 | "How to get those Crazy Eyebrows under control?" | `general` | Assumes something about the asker, not the answerer. It's a how-to request, which is a quality problem (parked below). |
| 23 | "People who like living in small towns over big cities, why?" | `fixable` | The filter is a preference; everyone has one. "Would you rather live in a small town or a big city, and why?" |
| 24 | "What was it like going out with a woman taller than you?" | `fixable` | Aimed without addressing (asks your own dating experience). The point is the height difference, not the gender, and it's a common experience. |

## Parked: not a directedness problem

Questions with a quality problem, collected for a possible later filter or model (maybe ADR 013). Don't let these change the directedness label.

- "How to get those Crazy Eyebrows under control?": a how-to / advice request. Maybe a layer 1 rule ("How to …").
- "Pretty women who used to be ugly, how do you feel about it?": insulting framing ("ugly").

## Changelog

- 2026-10-24: first version. Cases 1–7 and 14 decided; 8–13 open.
- 2026-10-24: case 11 → `unsalvageable`. `fixable` now includes questions that need rewording, not just deleting the address, as long as the rewrite asks the same thing. Added the "aimed without addressing" rule.
- 2026-10-24: decided 8, 9, 10, 12, 13; replaced their reasons. Case 14 confirmed `general`.
- 2026-10-24 (during test labelling): added the filter-type table, the rules section (gender built in, removing the gender isn't the end, stacked filters, reword limits, assuming vs aiming, asker vs answerer), cases 15–24, "If you…" as a filter form, and the parked list.
