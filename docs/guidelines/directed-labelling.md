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

**About a group vs aimed at a group: who is the question asking?** Ask whether the question wants *your own* experience or taste ("what's it like for you", "what do you…", "your…"), or asks *about* a group ("Do a lot of men…", "Is it frowned upon if a man…", "Why do women…"). Only the first is aimed. Mentioning men, even in every word, doesn't make a question aimed at men (cases 1, 25, 26). This was the most common slip in the kappa check: test questions had been labelled `fixable` when they only talked *about* men.

**"Guys" is gendered language.** When "guys" is used to address people ("you guys", "Guys, …", "Let's be honest guys"), it addresses men, so the question is aimed → at least `fixable` (cases 2, 27). This is a deliberate choice: casual "guys" isn't treated as gender-neutral. When "guys" is a noun *about* a group ("Do guys piss during…", "special forces guys"), use the about-vs-aimed check instead; it's usually `general`.

**A question can be aimed at a group without addressing it.** If it asks for a group's *own* tastes or experiences, only that group can answer from their own life, so it counts as aimed even with no "Ladies," up front (case 11). Compare case 1: asking *why* a group does something is an opinion anyone can give.

**Is the gender built into the question, or just who's being asked?** If the gender is just who's being asked, removing it leaves the question intact → `fixable` (cases 8, 10). If the gender is built into the question, removing it removes the point → `unsalvageable` (case 15).

**Removing the gender isn't the end of the check.** After the gender comes out, look at what's left. If what's left is still a trait not everyone has, it's `unsalvageable` (cases 16, 17).

**When filters stack, every filter has to pass.** One trait-type filter is enough to make it `unsalvageable` (case 18).

**A reword can't change the specific thing being asked about.** "Spanish" → "any language" is a different question (case 19). Toning down exaggeration is fine when it's the same situation ("evil" → "toxic", case 21), but not when it changes who you have to be to answer ("used to be ugly" → "had a glow-up", case 17).

**Assuming something isn't the same as aiming.** Nearly every question assumes something ("your first job", "your parents"). Assuming a common situation → `general` (case 20). Assuming a rare one counts as aimed without addressing ("What's it like raising twins?" → `unsalvageable`).

**An assumption about the asker isn't about the answerer.** "How to get my crazy eyebrows under control?" assumes the *asker* has crazy eyebrows. Anyone can answer it → `general` (case 22).

**Label directedness only.** A question can be boring, badly written, gossip or not in English and still be `general`. Quality is a separate problem from this label; park those questions at the bottom of this file. Content level is also separate: a sexual question addressed to "Ladies," is still just `fixable` here; SFW/NSFW is handled elsewhere (ADR 011).

## Edge cases

Cases marked **(T)** are test-set questions. That's fine for you, but **never use them as examples in a Llama prompt** (ADR 012), and keep this table closed while relabelling.

| # | Example | Call | Why |
|---|---|---|---|
| 1 | "Why do men fake tender moments?" · "Who has an easier life, men or women?" | `general` | About a group, not aimed at one. Anyone can give an opinion. |
| 2 | "Which AI do you guys use the most?" | `fixable` | "You guys" is gendered language, so it addresses men. Removing it leaves a question anyone can answer. (Changed from `general`, 2026-11-10.) |
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
| 15 (T) | "When you're hanging out with just your male friends, do you feel the need to close the door when using the bathroom?" | `unsalvageable` | Gender is built into the question. It's asking whether guys drop privacy around other guys; without "male" that's gone. Guys' night deck. |
| 16 (T) | "Women who have curly hair and don't like it, how do you deal with it?" | `unsalvageable` | The gender can come out, but curly hair is still a trait not everyone has. Deck tag: other, not girls' night. |
| 17 (T) | "Pretty women who used to be ugly, how do you feel about it?" | `unsalvageable` | The gender can come out, but "used to be ugly, now pretty" is a trait you have to see in yourself. "Had a glow-up" softens it into a different question. |
| 18 (T) | "If you're an extrovert, how did you find your introverted wife?" | `unsalvageable` | "Wife" → "partner" is fine, but it stacks two filters: you're an extrovert *and* your partner is an introvert. |
| 19 (T) | "If you study Spanish, what is your motivation behind it?" | `unsalvageable` | A rare activity. Making it answerable means changing "Spanish" to "a language", which is a different question. |
| 20 (T) | "What has your pet accidentally trained you to do without you even realizing it?" | `general` | No filter. It assumes a common situation; most people have had a pet at some point. |
| 21 (T) | "People who have an evil family member, how do you deal with them?" | `fixable` | A common experience. "Is there a family member you really can't stand? How do you deal with them?" is the same situation, less exaggerated. |
| 22 (T) | "How to get those Crazy Eyebrows under control?" | `general` | Assumes something about the asker, not the answerer. It's a how-to request, which is a quality problem (parked below). |
| 23 (T) | "People who like living in small towns over big cities, why?" | `fixable` | The filter is a preference; everyone has one. "Would you rather live in a small town or a big city, and why?" |
| 24 (T) | "What was it like going out with a woman taller than you?" | `fixable` | Aimed without addressing (asks your own dating experience). The point is the height difference, not the gender, and it's a common experience. |
| 25 (T) | "Do a lot of men use toys?" | `general` | Asks *about* men, not men's own experience. Anyone can have an opinion. (Adjudicated from `fixable`, 2026-11-10.) |
| 26 (T) | "Is it frowned upon if a man has a praise & humiliation kink?" | `general` | An opinion about men, not aimed at them. (Adjudicated from `fixable`.) |
| 27 (T) | "How do you guys know if you are healthy?" · "Let's be honest guys, what's the dumbest thing you've done because of "the urge"?" · "What do you guys think of UK wanting to split up?" · "Guys idk but is overthinking…" | `fixable` | "Guys" as an address is gendered language. Strip it and anyone can answer. |
| 28 (T) | "What does being mature actually mean to you as a man?" | `fixable` | "As a man" is a filter, so it's aimed (not `general`). "What does being mature mean to you?" keeps the question. |
| 29 (T) | "Men, what's something you consider "princess treatment" that women would consider the bare minimum?" | `unsalvageable` | Gender is built in: it's about the gap between men's and women's expectations. Guys' night deck. |
| 30 (T) | "For those who don't want children, what made you realize parenthood wasn't for you?" | `fixable` | The filter is a preference. "Do you want kids someday? What made you feel that way?" |
| 31 (T) | "Ladies, do you wear it once and take it back?" | `fixable` | Plain address; returning clothes isn't gendered. The vague "it" is a quality problem (parked). |
| 32 (T) | "How would you be able to afford insurance working part time but not being able to be on your parents plan?" | `general` | Not aimed; the situation is the asker's. An advice request (parked). |
| 33 | "Men, what's it like to open up to your woman only for her to ignore you or act as if what you're sharing is insignificant?" | `fixable` | Both layers pass: "Men," is only who's asked, and being dismissed by a partner is a common experience. "What's it like to open up to your partner, only for them to ignore you?" |
| 34 | "Men who became "ready" after ending a long-term relationship: did you ever feel guilty?" | `unsalvageable` | The gender can come out, but the experience is a specific two-part one (ended a long relationship, *then* became ready). |
| 35 | "Does any tall man here have a much taller mom, like at least 4" shorter than his mom?" | `unsalvageable` | Two trait filters stacked: tall man, and a mum taller than you. |
| 36 | "Notting Hill carnival. Man jumped in a canal… What exactly happened?" · "What happens to all of the graduates from community college game development programs?" | `general` | Not aimed. Factual or news questions, a quality problem (parked). |

## Parked: not a directedness problem

Questions with a quality problem, collected for a possible later filter or model (maybe ADR 013). Don't let these change the directedness label.

- "How to get those Crazy Eyebrows under control?": a how-to / advice request. Maybe a layer 1 rule ("How to …").
- "Pretty women who used to be ugly, how do you feel about it?": insulting framing ("ugly").
- "Ladies, do you wear it once and take it back?": vague "it" that refers to something missing from the title.
- "How would you be able to afford insurance working part time…": an advice request, and US-specific.
- "Notting Hill carnival… What exactly happened?" · "What happens to all of the graduates from community college game development programs?": factual or news questions, not conversation questions.

## Changelog

- 2026-10-24: first version. Cases 1–7 and 14 decided; 8–13 open.
- 2026-10-24: case 11 → `unsalvageable`. `fixable` now includes questions that need rewording, not just deleting the address, as long as the rewrite asks the same thing. Added the "aimed without addressing" rule.
- 2026-10-24: decided 8, 9, 10, 12, 13; replaced their reasons. Case 14 confirmed `general`.
- 2026-10-24 (during test labelling): added the filter-type table, the rules section (gender built in, removing the gender isn't the end, stacked filters, reword limits, assuming vs aiming, asker vs answerer), cases 15–24, "If you…" as a filter form, and the parked list.
- 2026-11-10 (after kappa 0.68): added the "about vs aimed" check and the casual "guys" rule, cases 25–36, marked test-set cases with (T), and added three parked categories (vague "it", advice requests, factual/news questions). Test labels for cases 25–26 adjudicated to `general`.
- 2026-11-10: "guys" is gendered language. Used as an address it means the question is aimed at men (at least `fixable`); as a noun about a group, it goes through the about-vs-aimed check. Case 2 → `fixable`. Case 27 → `fixable`: two test labels back to their original `fixable`, two adjudicated from `general`.
