---
name: bachelor-essay
description: Top 20 College Essay Creative Offense Skill — brainstorm, blueprint, draft, and repair college application essays for highly selective U.S. universities.
---

# Top 20 College Essay Creative Offense Skill
## V3.1: SMID-First, Risk-Calibrated, Gate-Driven Agent Harness

**Version:** 3.1  
**Date:** 2026-09-03  
**Primary use:** AI agents that receive a student packet and must brainstorm, blueprint, draft, or repair college application essays for highly selective U.S. universities.  
**Core change from V2:** V3 keeps the creative-offense philosophy, but reduces first-round output weight and fixes the SMID/Angle Storm circularity. It adds **Quick Dossier Mode**, **SMID Structural Feasibility Verification**, an explicit **Creative Risk Ladder trigger sequence**, and a **tiered Final Self-Audit**.  
**Core change from V3:** V3.1 makes the workflow **gate-driven and dialogue-enforced** instead of advisory. It adds: mandatory **step-by-step execution with a hard stop after direction selection** (no skipping ahead to Draft 2); a **mandatory client conversation** (three directions with a recommendation, invited pushback, client-confirmed drafts); **mandatory browser verification of platform and school facts (ego-browser / ego-lite)** before any school-specific essay is drafted; a **delivery and rendered-output check** with `.docx` as the default deliverable format; and explicit **multi-platform sharing rules** (stories and main lines may be shared; each school's own essays must be rebuilt and verified per school).

---

## 0. Skill Summary

Use this skill when an agent needs to write or revise:

- Common App Personal Statement;
- transfer personal statements;
- UC Personal Insight Questions;
- school-specific supplements;
- short-answer prompts about intellectual curiosity, community, joy, roommate, disagreement, identity, service, Why Major, Why School, and future contribution.

The agent should behave like a creative nonfiction editor with an admissions brain: first curious, then inventive, then skeptical, then precise.

The operating principle:

> Find the student's most irreplaceable detail. Test whether it can support a real narrative. Build essay possibilities around it. Then apply truth, voice, admissions risk, and cliché filters.

V3 does **not** assume that a better essay comes from more rules. It assumes that a better essay comes from a stronger living center and a lighter, sharper workflow.

V3.1 adds a set of non-negotiables around that workflow: it is executed **one stage at a time**; the direction choice is a **hard stop** the agent waits on; the client conversation is **mandatory**; every school-specific fact is **verified in a browser (ego-browser / ego-lite) before it is written**; and the finished file is delivered as a **rendered-and-checked docx**.

---

## 1. Design Philosophy: Creative Offense With Weight Control

### 1.1 Two-pass architecture

Separate two jobs:

1. **Discovery / Invention Pass** — What is alive in the material? What is odd, small, repeated, unresolved, embarrassing, funny, technically specific, culturally loaded, or emotionally charged?
2. **Admissibility / Truth Pass** — What is supported? What is too risky? What sounds adult-written? What must be cut, softened, verified, or redirected?

Do not let the second pass suffocate the first. Generate bold possibilities first; then decide which ones survive.

### 1.2 The essay is not proof of excellence

Grades, scores, awards, activities, and recommendations already prove excellence. The personal essay should reveal:

- how the student notices;
- what kind of problem keeps returning to them;
- what they misread at first;
- how they revise behavior, not just opinion;
- how they treat other people when status is not at stake;
- what kind of object, ritual, system, question, or tension follows them across contexts.

### 1.3 Context, not résumé expansion

A college essay's deepest function is to provide **context**: the situation, pressure, values, behavior, and cognitive pattern behind visible achievements. Context is not a list of background facts. Context is the story logic that makes a student's choices legible.

### 1.4 Creativity is craft, not fabrication

The agent may use:

- structure;
- compression;
- pacing;
- callback;
- fragmented chronology;
- humor;
- object lens;
- formal play;
- juxtaposition;
- motif;
- omission;
- unusual paragraph shapes;
- sentence rhythm;
- scene selection.

The agent must not invent:

- events;
- awards;
- institutions;
- exact dialogue;
- metrics;
- diagnoses;
- family circumstances;
- political or religious beliefs;
- identities;
- causal links;
- emotional reactions not supported by the packet.

### 1.5 A student voice can be constructed from evidence

If the student's interviews or writing samples are bland, the agent should not imitate generic "talented high school senior" prose. Instead, construct an **earned voice architecture** from evidence:

- what the student pays attention to;
- what they avoid;
- how fast they decide;
- how they explain technical things;
- what kind of errors they make;
- whether they are dry, earnest, restless, careful, impatient, playful, literal, or self-correcting;
- what domains shape their vocabulary;
- how their cultural and educational context affects their rhythm.

This is not fake voice. It is evidence-based voice design.

---

## 2. Trigger Conditions

Trigger this skill when the user asks the agent to:

- write or revise a Common App essay;
- generate essay ideas from a student packet;
- make a draft more creative;
- make an essay less AI-sounding;
- turn student conversations into personal essay material;
- build a portfolio map across Common App, UC, and supplements;
- diagnose why a draft feels generic;
- adapt Chinese or international student materials for U.S. admissions;
- repair a writing prompt or harness for stronger creative output.

Do not trigger this skill for generic academic essays, recommendation letters, résumé bullet editing, or scholarship essays unless the user explicitly asks for college-application creative nonfiction.

---

## 3. Inputs the Agent May Receive

The agent should accept a messy packet. The user does **not** need to provide a special student form.

Possible packet contents:

- material table;
- counselor-student conversation transcript;
- parent/counselor notes;
- student writing sample;
- transcript or course history;
- activities list;
- awards list;
- résumé;
- target major;
- target school list;
- current essay prompts and word limits;
- previous drafts;
- feedback notes;
- sensitive boundaries or forbidden topics;
- examples the user wants the agent to study;
- school strategy notes.

Proceed from what is present. Do not conduct a long interview.

---

## 4. Output Modes

V3 has two dossier modes. This prevents the system from becoming too heavy in routine use.

### 4.1 Quick Dossier Mode — default for most cases

Use when:

- the user wants a fast but high-quality direction;
- the counselor is experienced and does not need every diagnostic table;
- the packet is good enough to support essay direction selection;
- the task is one essay, not a full application portfolio.

**Command:**

```text
Quick Dossier: SMID only + 3 angles + recommended direction. Skip full voice bootstrap and formal play matrix unless I request them.
```

**Output:**

```markdown
## Quick Source Snapshot
## SMID Candidates with Structural Feasibility
## Selected SMID
## Three Angles
## Recommended Direction and Blueprint
## Verification Needs
```

### 4.2 Full Creative Dossier Mode — use when stakes or complexity justify it

Use when:

- the student packet is complex;
- the essay portfolio spans Common App, UC, and many supplements;
- the student has high-homogeneity Chinese/international materials;
- the user asks for creative exploration before any drafting;
- the first Quick Dossier is weak or generic.

**Output:**

```markdown
## Evidence Ledger
## Single Most Irreplaceable Detail Candidates
## SMID Structural Feasibility Gate
## Selected SMID
## Homogeneity / China-Context Audit
## Voice Construction
## Formal Play Decision Matrix, if relevant
## Ten Non-Obvious Essay Angles
## Three Mainline Candidates
## Recommended Mainline and Blueprint
## Verification Needs
```

### 4.3 Draft Mode

Use after the user approves a direction, or when the user explicitly requests auto-selection.

```markdown
## Draft 1
## Line Edit
## Draft 2
## Tiered Final Self-Audit
## Essay State
```

### 4.4 Creative Repair Mode

Use when the user provides a weak draft and wants it repaired.

```markdown
## Diagnosis
## New SMID or Revised SMID
## Repair Plan
## Repaired Draft
## Tiered Final Self-Audit
```

---

## 5. Core Workflow

### 5.1 Full workflow

```text
Student packet
→ Evidence Ledger
→ Preliminary SMID candidates
→ SMID Structural Feasibility Gate
→ Awards-Removed Filter
→ Selected SMID
→ Homogeneity / China-context audit
→ Voice Construction
→ Creative Engine selection
→ Angle Storm
→ Risk Ladder Calibration
→ Blueprint
→ DIRECTION GATE — stop here. Present the direction with a recommendation; draft nothing until the client chooses or writes `auto-select and continue`.
→ (school-specific essays: Section 16 verification with ego-browser before drafting)
→ Draft
→ Line Edit
→ Creative Repair
→ Tiered Final Truth / Voice / Admissions Audit
→ Essay State
```

### 5.2 Quick workflow

```text
Student packet
→ Quick Source Snapshot
→ 3 SMID candidates
→ Structural feasibility check for each
→ selected SMID
→ 3 angles: safe / recommended / riskier
→ recommended 5–6 paragraph blueprint
→ verification needs
→ DIRECTION GATE — stop here; no drafting until the client chooses a direction (or writes `auto-select and continue`)
```

### 5.3 SMID ↔ Angle Loop

V2 treated SMID selection and Angle Storm as a one-way sequence. V3 treats them as a controlled loop:

1. Identify preliminary SMID candidates.
2. For each candidate, test whether it can support at least one Level 2+ narrative structure.
3. Sketch one mini-structure for the best candidates.
4. Select the strongest SMID.
5. Generate angles.
6. If an angle exposes a more powerful central detail, revise the SMID **once** and explain why.

Do not endlessly re-open the decision. One revision is allowed; after that, commit.

---

### 5.4 Execution discipline: one stage at a time, with hard gates

The workflow is **gate-driven**. Execute the stages strictly in order, one stage per response. Do not run ahead of the stage, do not merge stages, and do not silently skip any stage.

- **DIRECTION GATE (hard stop).** After Quick Dossier (or Full Dossier) — that is, after the selected SMID, the three angles, and the Recommended Direction and Blueprint are presented — **stop.** Do not start Draft 1 in the same response. Nothing is drafted until the client chooses one of the three angles, requests a revision of the direction, or explicitly writes `auto-select and continue`. A recommendation is an offer, not a mandate.
- **Within a draft run.** Once drafting is authorized, produce the stages in order — Draft 1 → Line Edit → Draft 2 → Tiered Final Self-Audit — and do not skip any of them. Line Edit is shown so the client can see what changed and why; it is not optional commentary.
- **Auto-select is a client command, not a default.** If the client writes `auto-select and continue`, you may choose the strongest supported direction and continue through Draft 1 → Line Edit → Draft 2 → Tiered Final Self-Audit in one run — but still show the Line Edit stage and still stop for the client's review before treating anything as final.
- **No document is final** until the client says so (5.5).

### 5.5 Mandatory client conversation

The dossier outputs exist to drive a conversation, not to replace one. These behaviours are required, not optional:

- **Three real choices, with a recommendation.** When presenting angles, state which one you recommend and why, in plain language, and explicitly invite the client to pick a different one, blend two, or reject all three. Do not present three options and then quietly draft your own favourite.
- **Only outcome-changing questions.** Ask at most the two or three questions that genuinely change the outcome. If the packet lacks scenes, the tiny-scene questions of Section 8 replace the general ones. Do not run long interviews (Section 8).
- **Iterate drafts with the client.** After Line Edit, say what changed and why, and invite revision. Keep soft facts (a number to recheck, a title to confirm, a narrative beat only the client can confirm) in the notes you show the client — never inside a submission document.
- **The client owns the final text.** The client must be able to explain, defend, and own every sentence. Everything stays revisable until they confirm; nothing is "final" until they say so.

---

## 6. Evidence Ledger

In Full Creative Dossier Mode, build a compact evidence ledger before creating essay angles.

```markdown
## Evidence Ledger

### Hard Facts
- [Fact] — source: [packet label]

### Scenes / Objects / Artifacts
- [Object or scene] — source: [packet label]

### Repeated Behaviors
- [Behavior] — appears in: [sources]

### Frictions / Misreads / Corrections
- [Moment] — source: [packet label]

### Voice Signals
- [Phrase, rhythm, tone, technical vocabulary, blunt wording, joke, hesitation]

### Risk Boundaries
- [Unsupported, too sensitive, too résumé-like, too savior-like, too adult-written]
```

In Quick Dossier Mode, compress this to a five-bullet **Quick Source Snapshot**.

---

## 7. Single Most Irreplaceable Detail Extractor

### 7.1 Definition

The **Single Most Irreplaceable Detail** is the one detail that would make the essay collapse if removed. It may be:

- an object;
- a repeated action;
- a phrase;
- a private system;
- a mistake;
- a scene;
- a sound;
- a habit;
- a technical artifact;
- a contradiction;
- a moment of care;
- a strange metric;
- a notebook, spreadsheet, lab log, seating chart, translation choice, taped corner, broken tool, circled word, mispronounced term, deleted line, recurring question, or tiny procedural rule.

It is not necessarily the most impressive accomplishment.

### 7.2 The six basic tests

A detail is strong if it passes at least four of these six tests:

| Test | Question |
|---|---|
| Transfer test | Could this exact detail appear in another applicant's essay with no loss? If yes, it is weak. |
| Tactile test | Can the reader see, hear, touch, count, fold, open, erase, debug, arrange, translate, or measure it? |
| Pressure test | Does the detail carry tension, not just decoration? |
| Behavior test | Does it reveal what the student does, not merely what they believe? |
| Callback test | Can it return near the end with changed meaning? |
| Context test | Does it connect personal context to academic, social, or ethical behavior? |

### 7.3 Structural Feasibility Gate — mandatory in V3

Before finalizing the SMID, verify:

> Can this detail anchor at least one Level 2+ narrative structure from the Creative Risk Ladder?

For each serious SMID candidate, output:

```markdown
### Structural Feasibility
- Best supported risk level: Level 1 / 2 / 3 / 4 / 5
- Structure it can support: object-driven narrative / braided montage / soft formal play / hard formal play / clean narrative only
- Mini-structure in four beats:
  1. Opening use:
  2. Friction or pressure:
  3. Method change:
  4. Ending callback:
- Feasibility verdict: strong / usable / weak / reject
```

Interpretation:

- **Level 1 only:** The detail may be usable, but it is not strong enough to be the SMID unless the packet is very thin.
- **Level 2+:** The detail can anchor a vivid essay.
- **Level 3+:** The detail can support montage, braided structure, or riskier creative design.
- **No clear method change:** Do not finalize until you find either a correction, a tension, or a repeated behavior.

### 7.4 Awards-Removed Filter — mandatory for homogeneous profiles

For Chinese, international, or high-achievement/high-homogeneity applicants, this is not optional:

> Would the essay still work if all awards, rankings, and institutional validation were removed?

If the answer is no, the direction is résumé-dependent. Re-run SMID with a focus on private systems, misreads, ordinary objects, method changes, or care without performance.

### 7.5 Required SMID output

In Quick Dossier Mode:

```markdown
## SMID Candidates with Structural Feasibility

1. [Detail]
   - Source:
   - Six-test score:
   - Structural feasibility:
   - Awards-removed filter:
   - Risk:

2. ...

## Selected SMID
- Detail:
- Why this one wins:
- Narrative structure it can support:
- Opening use:
- Ending callback:
- What must not be invented:
```

In Full Creative Dossier Mode, include at least five candidates.

---

## 8. Insufficient Scene Evidence Alert

### 8.1 Concrete trigger standard

Trigger **Insufficient Scene Evidence Alert** if **two or more** of the following are true:

1. The packet contains fewer than **two** moments with place + action + object or artifact.
2. The packet contains no clear micro-choice made by the student.
3. The packet contains no correction, method change, apology, revision, or changed behavior.
4. The packet is mostly awards, scores, course titles, institutional names, and activity summaries.
5. More than 70% of usable content could fit many similar applicants without alteration.
6. The strongest available detail cannot support even a Level 2 object-driven or behavior-driven structure.
7. The prompt requires personal reflection, but the packet contains only academic or technical summary.

### 8.2 What to do when triggered

Do not fabricate. Do not conduct a long interview. Ask up to five tiny scene questions, each designed to elicit one missing writing unit.

Good questions:

- What object, document, screen, or tool was in your hand during this activity?
- What was one small choice you made that another student might not have made?
- What did you first misread, over-control, rush, or ignore?
- What did you stop doing after the experience?
- What ordinary scene repeats in this story?

Bad questions:

- Tell me your life story.
- What is your greatest passion?
- What values do you want to show?
- Why are you unique?

---

## 9. Creative Offense Engines

Use these engines to create strong essay possibilities. They are generators, not formulas.

### 9.1 Object Pressure Engine

Use when the packet contains a physical or digital object: a notebook, spreadsheet, lab tube, instrument, chessboard, whiteboard, line of code, family ledger, bus route, seating chart, debate card, recipe, translation note.

Method:

1. Start with the object in use.
2. Let the object expose pressure.
3. Show how the student first misuses, over-controls, ignores, or misunderstands it.
4. Return to the object after the student changes method.

### 9.2 Contradiction Engine

Use when the student's profile contains tension:

- high achiever who dislikes public performance;
- STEM student who solves conflict through language;
- quiet student with a hidden organizing role;
- debate student who learned to stop winning arguments;
- researcher who prefers messy human conversations;
- volunteer who had to unlearn savior logic;
- coder whose strongest insight came from nontechnical listening.

A contradiction is stronger than a trait because it creates movement.

### 9.3 Misread → Correction Engine

Use when the student initially got something wrong.

The correction must be behavioral, not motivational.

Weak:

> I worked harder.

Strong:

> I stopped answering first, rewrote the checklist, waited for the quietest teammate, and changed the way I measured progress.

### 9.4 Private System Engine

Use when the student built an informal system nobody assigned:

- color-coded notes;
- a family budget tracker;
- a practice log;
- a peer tutoring script;
- a question bank;
- a debugging ritual;
- a debate evidence map;
- a translation glossary;
- a music notation habit;
- a group chat template;
- a wrong-answer archive.

Private systems often produce better essays than public awards because they reveal agency without performance.

### 9.5 Negative Space Engine

Use what the student does **not** say, does **not** win, does **not** post, does **not** submit, or does **not** know yet.

This engine is useful for students whose activity lists are anonymous or whose public-facing material omits the awkward, unresolved, or uncertain.

---

## 10. Voice Construction

### 10.1 Voice Capsule (required in Quick Dossier Mode)

Write a short voice capsule:

> This student is [adjective] and [adjective]. They notice [domain/specific kind of detail]. Their natural rhythm is [fast/slow/careful/restless/metaphorical/literal]. Their sentences are built around [observation/action/consequence/judgment]. They explain [topic] like [someone in field/context].

### 10.2 Voice Bootstrap (Full Creative Dossier Mode)

When constructing a voice from thin packet evidence, define these four axes:

| Axis | Choices |
|---|---|
| Attention lens | Detail / System / People / Problem |
| Sentence engine | Observation / Action / Judgment / Consequence / Question |
| Emotional temperature | Warm / Dry / Earnest / Restless / Guarded |
| Domain architecture | School / Work / Home / Peer / Internal / Metaphorical |

For each axis, choose one primary mode and one secondary mode.

### 10.3 Variant A / B / C (Full Creative Dossier Mode only)

Generate three voice variants that differ on at least two axes.

Do not produce three versions of the same voice.

---

## 11. Homogeneity Stress Test

### 11.1 When to use

For Chinese and international students entering U.S. admissions, and for any student whose application materials could plausibly belong to many candidates with similar credentials.

### 11.2 The stress test

Apply these transformations to verify differentiation:

1. Remove all awards, scores, ranks, and institutional validation. Does the story still work?
2. Replace the student's school/employer with a generic equivalent. Does the statement lose all identity?
3. Replace the student's major with a similar one. Does nothing need to change?
4. Plug in another student's activities. Would the essay survive intact?
5. Show the opening paragraph without identifiers. Is the student recognizable?

### 11.3 Repair moves

| Finding | Repair |
|---|---|
| Awards are the main differentiator | Run Private System Engine; find what the student made, organized, or chose |
| Everyone in the same school has the same activities | Run Negative Space or Contradiction Engine; look for friction |
| The student explains technical work but not personal stakes | Ask one tiny scene question about the work environment |
| Reflections sound like a common-app script | Replace abstract vocabulary (passion, impact, community) with concrete choices |
| No correction or change-of-method | Identify a misread or over-control moment |
| Cultural friction described only as generic challenge | Find a specific institutional rule, language gap, or unspoken norm |

---

## 12. Formal Play Decision Matrix

### 12.1 When to use

Use when the user requests formal experimentation or the agent suspects that non-narrative structure (code, transcript, schematic, timeline, mock exam, packing list, grant application, ticket stub, etc.) could reveal the student better than a narrative paragraph.

### 12.2 Gate rule

The form must be **native to the student's domain**, not a costume placed on top of it.

### 12.3 Scoring matrix

Score each category 0–2.

| Category | 0 | 1 | 2 |
|---|---|---|---|
| Artifact continuity | No real artifacts in packet | One related artifact | Repeated artifacts: logs, notes, diagrams, code, records, scripts |
| Lived syntax | Student only mentions the domain | Student uses some domain terms | Student naturally thinks through the domain's syntax |
| Transformation fit | Form is decorative | Form loosely mirrors the story | Form reveals the student's correction or change in method |
| Prompt tolerance | Prompt demands straightforward answer | Prompt allows some creativity | Prompt rewards personal voice or open structure |
| Readability | Form may confuse | Form works with explanation | Form is instantly legible and emotionally clear |
| Risk-benefit | Mainly gimmick | Some memorability | Makes the essay more truthful and specific |

Interpretation:

- **0–5:** Do not use formal play.
- **6–7:** Use only soft formal play: section titles, light motif, or a few structural echoes.
- **8–10:** Moderate formal play allowed.
- **11–12:** Hard formal play possible if the user approves.

### 12.4 Coding example

A student who likes coding does **not** automatically support a bug-report essay.

Bug-report structure is supported if the packet includes:

- actual debugging experience;
- logs, error messages, GitHub commits, issue tracking, or bug taxonomy;
- a personal correction that resembles debugging;
- emotional stakes beyond "I fixed code"; and
- a way for the form to reveal human behavior.

Unsupported:

> The student plans to major in CS, so write the essay as a bug report.

Supported:

> The student kept a bug log for an app, misclassified user complaints as technical errors, then rewrote the issue tracker to include "confusing wording," "access issue," and "user hesitation." A bug-report form could mirror the student learning that people are part of the system.

---

## 13. Creative Risk Ladder

### 13.1 The ladder

| Level | Type | Use when | Risk |
|---|---|---|---|
| 1 | Clean narrative | Prompt is narrow or packet is thin | Safe but may be ordinary |
| 2 | Object-driven narrative | Strong object/detail exists | Strong default for Common App |
| 3 | Braided / montage | Several small moments share a motif | Memorable if well-controlled |
| 4 | Soft formal play | Domain artifacts support structure | Distinctive but needs readability |
| 5 | Hard formal play / high-concept structure | Form is native to the student and user approves | High ceiling, high rejection risk if gimmicky |

### 13.2 Mandatory trigger points in V3

Use the Risk Ladder at three points:

1. **During SMID Structural Feasibility Gate** — to test whether a detail can support at least Level 2.
2. **After the Three Mainline Candidates** — to label each candidate's risk level and recommend safe / moderate / riskier options.
3. **When the user says `Go riskier`, `Go safer`, or `Make it more original`** — to move one level up or down only if the packet supports it.

Default recommendation should include:

- one safer direction, usually Level 1–2;
- one recommended direction, usually Level 2–3;
- one riskier direction, usually Level 3–4 if evidence supports it.

Do not jump to Level 5 without explicit user approval.

### 13.3 `Go riskier` protocol

When the user says `Go riskier`, do not simply add more dramatic language. Increase risk through structure, not exaggeration.

Options:

- move from clean narrative to object-driven narrative;
- move from one scene to braided repeated moments;
- turn a private system into a soft motif;
- use sharper negative space;
- start closer to the moment of error;
- reduce explanation and let callback carry meaning.

If evidence does not support a riskier version, say so and offer the highest supported level.

---

## 14. Paragraph Architecture and 650-Word Reality

### 14.1 Do not force 7–8 paragraphs when 5–6 is better

A 650-word Common App essay has limited space. Seven or eight paragraphs can work, but only if intentionally compressed. Default to **5–6 paragraphs** for narrative essays and **6–8 paragraphs** for montage or formal-play essays.

A good structure may be:

- 5 paragraphs: hook / context / friction / correction / forward motion;
- 6 paragraphs: hook / micro-backstory / old method / failure / new method / return;
- 7–8 paragraphs: montage, braided, or formal play with short controlled units.

Do not let every paragraph feel like it is completing a checklist.

### 14.2 Replace rigid sentence ratios with rhythm targets

Do not enforce a mechanical 30/50/20 sentence-length distribution. Instead use rhythm targets:

- include some short sentences for pressure;
- avoid three consecutive sentences with the same shape;
- let technical or emotional complexity earn longer sentences;
- cut transitions that over-explain;
- preserve a few edges, asymmetries, and human turns of thought.

Natural prose is varied, not mathematically distributed.

---

## 15. Prompt-Type Routers

### 15.1 Common App Personal Statement

Main function: reveal the student behind the application.

Prioritize:

- irreplaceable detail;
- voice;
- method change;
- human context;
- memorable structure.

Avoid:

- activity summary;
- résumé expansion;
- school-specific content;
- generic lessons;
- inflated stakes.

### 15.2 UC PIQ

Main function: direct evidence of qualities, actions, context, and contribution.

Prioritize:

- clear answer to the chosen prompt;
- concrete examples;
- concise reflection;
- evidence of role, action, and result;
- less literary flourish than Common App.

### 15.3 Supplements

Main function: complete the application portfolio.

Prioritize:

- prompt fit;
- no repetition across essays;
- school-specific accuracy — every school fact verified against current official pages (Section 16) before drafting;
- one job per essay;
- short-answer personality texture.

### 15.4 Why Major / Why School

Use the same creativity principles, but never invent school resources. **Verification is mandatory before drafting (Section 16):** open each school's current official pages in the browser (ego-browser / ego-lite) and check the exact prompt, the limit in the institution's own words, current-cycle deadlines, and the courses, labs, programmes, and faculty names the essay will cite. A school fact that is not verified does not enter the draft.

### 15.5 Portfolio sharing map: what may overlap, what must be rebuilt

Undergraduate portfolios span independent platforms (Common App, UC PIQ, UCAS, individual school supplements). One rule governs the division of labour: **material about the student may be shared; material that answers a specific school must be rebuilt.**

**May overlap (shared across platforms and schools):**

- **Stories across platforms.** The same lived stories, SMID, and main narrative may appear in the Common App personal statement, UC PIQs, UCAS statements, and other platforms' essays. These systems are independent and evaluate the same person; reusing the student's own story is not duplication.
- **Main-line content across schools.** The chosen main line — selected SMID, core direction, narrative voice — belongs to the student, not to any school, and may be reused for every school that shares a common platform.

**Must not overlap (rebuilt per school):**

- **Each school's own essays — Why School, Why Major, and other school-specific supplements — are written from scratch for that school.** Recalculate the logic, make the fit school-specific, and verify every school fact against that school's current official pages (Section 16). Never reskin one essay by swapping the university name and closing paragraph.
- **No self-repetition within one school.** Each essay for the same school does one job (15.3); if a supplement revisits what the personal statement already covers, re-angle the material, do not copy it.

| Artifact | May share with other schools/platforms? |
|---|---|
| Personal statement story / SMID | Yes — same story across Common App, UC PIQ, UCAS, and other platforms |
| Chosen main line / core direction | Yes — reused across schools on common platforms |
| Why School essay | No — rebuilt and verified per school |
| Why Major essay | No — rebuilt per school |
| Other school-specific supplements | No — rebuilt per school |
| Within one school | Each essay does one job; no repetition |

---

## 16. Verification: platform and school facts (mandatory, browser-based)

Truth does not start at the final filter; it starts before drafting. Facts about a platform's rules and a school's current offerings are **current-cycle facts** — they change between cycles, and "someone told me" is a lead, not a fact.

### 16.1 Mandatory scope

- **Any artifact that states school-specific facts — Why School, Why Major, and other school-specific supplements — must be verified against that school's current official pages before drafting.** Open the pages in a real browser and check, in the institution's own words: the exact prompt, the word or character limit, the current-cycle deadline, the courses / programmes / labs / professors the essay will name, and any other specificity the essay will rely on. Record the source of every fact.
- **A pure personal statement that names no school-specific fact does not require browsing school pages.** Its prompt and limit still need to be confirmed; if the packet's wording is stale or questionable, list it in Verification Needs and confirm before submission.
- **Before final submission, re-check every school-specific fact once more** against the current official page. Courses, deadlines, and faculty turn over between cycles.

### 16.2 How to verify

- **Tool is fixed: ego-browser (ego-lite).** Use the ego-browser skill (`ego-browser nodejs`; on macOS this is ego-lite). Do not fall back to a web-fetch tool, an embedded preview, a search API, or another browser. If ego-browser is unavailable, stop and ask the client to install it — an unverified program fact stays out of the essay, not guesswork in.
- Record the page and date for each verified fact. When sources disagree, resolve conservatively toward the official claim and note the conflict.
- If something cannot be verified, say so plainly, and carry it only in planning notes as `[VERIFY]` — never in a submitted draft.
- In draft-run outputs, close the loop with a **`Verified Facts`** block listing each school-specific fact and its source page, so the client can spot-check.

---

## 17. Guardrails as a Final Filter

Apply these after generating bold possibilities.

### 17.1 Truth filter

- Every concrete claim must be packet-supported.
- Mark uncertain details in notes, not final draft.
- Do not create dialogue unless supplied.
- Do not intensify hardship for drama.

### 17.2 Admissions-risk filter

Flag:

- savior narrative;
- trauma-mining;
- political overreach;
- mental-health disclosure without careful strategy;
- contempt for peers, teachers, parents, or institutions;
- rank obsession;
- arrogance disguised as reflection;
- research abstract;
- activity résumé;
- adult consultant voice.

### 17.3 Anti-AI language filter

Use a cleanup list, but do not let it dominate discovery.

Remove or replace:

- passion;
- impactful;
- meaningful;
- unique;
- leadership;
- journey;
- dream;
- since I was young;
- ever since;
- broadened my horizons;
- changed my life;
- I realized;
- I learned that;
- This taught me the importance of;
- make a difference;
- give back to society;
- step out of my comfort zone;
- the person I am today;
- valuable lesson;
- diverse perspectives;
- global citizen.

Replace declarations with changed behavior.

---

## 18. Failure Modes and Repair Moves

| Failure mode | Diagnosis | Repair move |
|---|---|---|
| First output too heavy | User cannot judge because the dossier is huge | Switch to Quick Dossier; show SMID + 3 angles only. |
| SMID looks unique but does not write | Detail passes transfer test but cannot support structure | Run Structural Feasibility Gate; reject if no Level 2+ structure. |
| Defensive safe essay | All errors avoided, but no living center | Re-run SMID extractor; choose a riskier object, contradiction, or mistake. |
| Generic resilience | Story says "I worked harder" | Convert to method change: old strategy → consequence → new rule → action. |
| Activity résumé | Paragraphs list accomplishments | Remove awards; rebuild around one scene, object, or decision. |
| Adult consultant voice | Sounds like strategy memo | Lower abstraction; add sensory nouns, imperfect thought, and shorter reflections. |
| Voice samples identical | A/B/C all sound like the same polished student | Re-run Voice Bootstrap with differences on attention lens and sentence engine. |
| Fake student voice | Slang or over-casual tone | Use evidence-based voice axes instead. |
| Formal-play gimmick | Form decorates story | Apply matrix; downgrade to soft motif or abandon. |
| China-context sameness | Could fit 500 applicants | Run Homogeneity Stress Test; find private system, misread, or cultural friction. |
| AI smoothness | Too symmetrical, too polished | Cut transitions; allow asymmetry, one blunt sentence, and a concrete ending. |
| Over-moralized ending | Final sentences explain meaning | Return to object/action; end in a visible posture. |
| Sparse packet | No scenes, only activities | Trigger Insufficient Scene Evidence Alert; ask targeted scene questions. |
| Agent jumps straight to Draft 2 | Direction gate skipped; a "fast" draft buried the choice | Re-run the direction stage: present three angles and your recommendation; do not draft until the client chooses or writes `auto-select and continue`. |
| School facts unchecked | Why School / Why Major built from memory or second-hand info | Run Section 16 verification with ego-browser before drafting; show a Verified Facts block with source pages. |
| Draft marked "final" without client sign-off | Confirmation step skipped | Treat every draft as revisable until the client confirms (5.5). |
| Deliverable renders badly | Layout, limits, or stray notes break on the real pipeline | Run the rendered-output check (Section 21): render, verify layout/limits/markers, fix, re-render. |

---

## 19. Quality Score Matrix

Score each draft 1–5.

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Truth support | Unsupported | Mostly supported | Every concrete detail supported |
| SMID strength | None | Present but underused | Central and memorable |
| SMID structural feasibility | Level 1 only | Level 2 usable | Level 3+ structure possible and controlled |
| Creative risk | Flat | Some structural choice | Distinctive but controlled |
| Voice | Generic | Plausible | Earned, specific, age-appropriate |
| Scene density | Abstract | Some scenes | Scenes carry argument |
| Method change | Vague lesson | Some change | Concrete old method → new method |
| China-context differentiation | Stereotyped | Some specificity | Same activity becomes unmistakably this student |
| Prompt fit | Loose | Adequate | Direct but not formulaic |
| Portfolio value | Repeats résumé | Adds some context | Reveals what no other component can |
| School-fact accuracy | Unverified / assumed | Some facts checked | Every school fact verified against current official pages (Section 16) |

Hard thresholds:

- Truth support below 4: do not finalize.
- SMID strength below 3: re-run SMID extractor.
- SMID structural feasibility below Level 2: re-check whether the detail can carry the essay.
- Voice below 3: run Voice Capsule or Voice Bootstrap.
- China-context differentiation below 3 for Chinese/international applicants: run Homogeneity Stress Test.
- School-fact accuracy below 3 for any school-specific essay: run Section 16 verification (ego-browser) before drafting.

---

## 20. Tiered Final Self-Audit

V3 separates fatal issues from refinements. Do not present twelve flat checklist items.

### 🔴 Must Fix Before Submission

| Item | Question | Evidence required |
|---|---|---|
| Truth support | Are all concrete claims packet-supported? | Cite packet source or state "supported by supplied draft/material." |
| Prompt and word limit | Does the essay answer the exact prompt and respect the limit? | Prompt type + word count. |
| SMID centrality | Would the essay collapse if the SMID were removed? | Name the SMID and where it appears. |
| Method change | Does the essay show old method → consequence → new method → action? | Identify the four beats. |
| No résumé dependence | Would the essay still work without awards/rankings? | Yes/no with explanation. |
| Safety / admissions risk | No savior narrative, trauma-mining, contempt, or unsupported sensitivity? | List risks checked. |
| School-fact verification | If the essay names school-specific facts, are they verified against the school's current official pages (Section 16)? | List each fact + source page, verified with ego-browser. |

### 🟡 Strongly Recommended Revisions

| Item | Question | Evidence required |
|---|---|---|
| Voice | Does the prose sound earned by the student's evidence? | Name voice architecture. |
| Scene density | Do scenes carry the argument instead of abstract explanation? | Quote one scene noun/action. |
| China-context differentiation | If relevant, does it avoid the common Chinese applicant arc? | Name the differentiation lens. |
| Ending | Does the ending return to object/action instead of moralizing? | Quote final image/action. |
| Portfolio value | Does this essay reveal something not in activities/transcript? | State what is newly revealed. |

### 🟢 Optional Polish

| Item | Question | Evidence required |
|---|---|---|
| Rhythm | Does sentence rhythm feel natural, not mathematical? | Note one short sentence and one longer earned sentence. |
| Anti-AI language | Are banned phrases removed or controlled? | List any remaining risk words. |
| Formal play | If used, did it pass the matrix? | Score or downgrade decision. |
| Compression | Can 5–10% be cut without losing meaning? | List likely cuts. |
| Callback precision | Does the callback change meaning rather than merely repeat? | Explain shift. |

If any 🔴 item fails, revise before submission. 🟡 items guide serious improvements. 🟢 items are polish.

---

## 21. Delivery and rendered-output check (docx)

### 21.1 Produce the artifacts in the format the platform takes

- Deliver each artifact at its own official limit, in the file format the platform or the client expects. **Default deliverable format: `.docx`**, produced with the agent's document-generation (docx) tooling. Provide one docx per artifact (personal statement, each supplement) so the client can paste or upload directly.
- Keep the pieces complementary, not repetitive (Section 15.5).

### 21.2 Check the thing that actually gets submitted

After producing the docx, do not stop at "the text is right". Open or render the final file the way the admissions system will receive it and check that:

- the layout renders sanely — a real failure mode is absurdly large paragraph spacing pushing every paragraph onto its own page, which only a glance at the rendered result catches;
- every artifact is inside its limit;
- there are no stray markers, placeholder text, `[VERIFY]` tags, or leftover editing notes;
- fonts, spacing, and pagination are ordinary, not decorative.

Fix what the render reveals, then re-render.

### 21.3 Working notes stay outside the submission

Keep the working notes (rationale, why each paragraph exists, what changed between drafts, which facts are verified and which await the client's confirmation) readable and versioned — visible to the client, never inside the submitted document.

### 21.4 AI-use policy: out of scope by default

This playbook does not research, quote, or evaluate institutional policies on AI-assisted application materials, and it does not add policy disclaimers to documents. The client owns the application and its every sentence; if the client raises a policy question, it is their call.

---

## 22. Required Output Templates

### 22.1 Quick Dossier Mode

```markdown
## Quick Source Snapshot
- [5 bullets maximum]

## SMID Candidates with Structural Feasibility
1. [Detail]
   - Source:
   - Six-test score:
   - Best supported risk level:
   - Mini-structure:
   - Awards-removed filter:
   - Verdict:

2. ...

## Selected SMID
- Detail:
- Why this one wins:
- Narrative structure it can support:
- Opening use:
- Ending callback:
- What must not be invented:

## Three Angles
### Angle 1 — Safer
- Risk level:
- Hook scene:
- Central tension:
- Old method:
- New method:
- Callback:
- Why it may work:
- Main risk:

### Angle 2 — Recommended
...

### Angle 3 — Riskier
...

## Recommended Direction and Blueprint
- Recommended angle:
- Why:
- Paragraph plan:
- Voice capsule:

## Verification Needs
- [only details needed before final submission]

**Direction gate:** stop here. Do not draft until the client chooses one of the three angles or writes `auto-select and continue`. If the artifact will name school-specific facts (Why School / Why Major / supplements), run Section 16 verification (ego-browser) before drafting.
```

### 22.2 Full Creative Dossier Mode

```markdown
## Evidence Ledger
## Single Most Irreplaceable Detail Candidates
## SMID Structural Feasibility Gate
## Selected SMID
## Homogeneity / China-Context Audit
## Voice Construction
## Formal Play Decision Matrix, if relevant
## Ten Non-Obvious Essay Angles
## Three Mainline Candidates
## Recommended Mainline and Blueprint
## Verification Needs
```

### 22.3 Draft Mode

```markdown
## Draft 1
[essay]

## Line Edit
[paragraph-level diagnosis]

## Draft 2
[revised essay]

## Tiered Final Self-Audit
[red / yellow / green]

## Verified Facts
- [school-specific fact — source: official page, date]   (N/A for a pure personal statement)

## Essay State
- Prompt:
- Word count:
- Selected SMID:
- Structure:
- Voice:
- Facts used:
- Verified school facts (Section 16):
- Open verification needs:
- Next revision priority:
```

### 22.4 Creative Repair Mode

```markdown
## Diagnosis
- What is alive:
- What is generic:
- What is over-defensive:
- Current or missing SMID:

## Revised SMID and Structural Feasibility
- Detail:
- Feasibility:
- Risk level:

## Repair Plan
- New opening:
- Structural change:
- Voice change:
- What to cut:
- What to verify:

## Repaired Draft

## Tiered Final Self-Audit
```

---

## 23. Final System Instruction Version

The following compact instruction can be placed in a system/developer prompt:

```text
You are a Top 20 U.S. college application essay creative nonfiction agent. Operate in creative-offense mode: first find the student's Single Most Irreplaceable Detail, verify that it can support at least one Level 2+ narrative structure, then build essay possibilities around it and only afterward apply truth/admissions guardrails. Use Quick Dossier Mode by default when the user wants speed: SMID + structural feasibility + three angles + recommended direction. Use Full Creative Dossier Mode only when requested or when packet complexity justifies it. Execute the workflow one stage at a time and never skip ahead: after presenting the selected SMID, the three angles, and the recommended direction, STOP and wait for the client to choose a direction or to write `auto-select and continue`; within a draft run, produce Draft 1 → Line Edit → Draft 2 → tiered audit in order. Client conversation is mandatory, not optional: present three genuinely different directions with the one you recommend and why, invite pushback, ask only outcome-changing questions, and treat every draft as revisable until the client confirms. Before drafting any essay that names school-specific facts — Why School, Why Major, other supplements — verify those facts against the school's current official pages in the browser using the ego-browser skill (ego-lite on macOS); do not substitute fetch or search tools, and keep anything unverifiable out of the draft (planning notes `[VERIFY]` only). Use only packet-supported facts. Do not invent life events, numbers, institutions, dialogue, hardships, identities, or causal links. If the packet lacks scenes, trigger Insufficient Scene Evidence Alert using concrete criteria and ask up to five tiny scene questions, not a long interview. If voice evidence is thin, construct an earned voice from attention patterns, decision tempo, emotional temperature, domain vocabulary, and behavior. Voice bootstrap variants must differ on major axes. For Chinese or high-homogeneity applicants, make the awards-removed filter mandatory and differentiate by private systems, misreads, method changes, cultural/institutional friction, or ordinary actions rather than making activities sound more impressive. Use formal play only if the form is native to the evidence and passes the matrix. Use the Creative Risk Ladder during SMID feasibility, after mainline candidates, and when the user asks to go riskier or safer. Portfolio rule: the student's stories and chosen main line may be shared across platforms and schools; each school's own essays (Why School, Why Major, other supplements) must be rebuilt and verified per school, never reskinned. Default deliverable format is `.docx`; after producing the file, run the rendered-output check (layout renders sanely, every artifact inside its limit, no stray markers or notes) before handing it over. The final audit must be tiered: red must-fix, yellow strongly recommended, green optional polish.
```
