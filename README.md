# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter sorts public posts from [r/workout](https://www.reddit.com/r/workout/)
by their main purpose. It assigns
`help_request` when the author wants advice for their own fitness situation,
`discussion_prompt` when they invite a broader conversation or other people's
experiences, and `sharing` when they mainly report an experience, result, or
view. I reviewed a 200-post dataset under this taxonomy and fine-tuned
DistilBERT on its training split.



---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### Community reading notes (Milestone 1)

Community: [r/workout](https://www.reddit.com/r/workout/). These provisional
distinctions come from posts brought from the front page. They are observations to potentially test,
not final labels.

- **Personal help request vs. open discussion:** There are posts like,"Gym progress and scared to
  eat." These are more about the author asking what to do with their situation. Constrastly, there are posts like "What's one fitness habit
  that made a bigger difference than you expected?" These are posts that invite everyone to share their own situation / experience.
- **Personal account vs. general recommendation:** There are some posts that are more personal anecdotes that recounts a specific gym
  interaction, while there are posts like "I don't know who needs to hear this..." which are more general messages (people should stay
  home from the gym when sick). There is also a sort of mix like, "Stubborn man realizes tracking food actually
  works." This combines a personal result with a broader lesson (could be hard to distinguish).
- **Existing plan for review vs. help starting:** Posts like "I need help since im
  starting a new split" provides a complete PPL/UL schedule for feedback. Posts like
  "Home dumbell workout as a newbie" asks how to begin with home equipment.
- **Detailed context vs. sparse context:** Some posts include schedules, sets,
  goals, and constraints. There are also very broad / less personal posts like "What are the signs someone uses steroids?
 This may affect how answerable a post is, whatever its topic (less personally tailored, as well as posts that are more "for fun" and not personal).

Topics also vary across training plans (including splits), food and
supplements, motivation, progress, and gym culture. A topic-only taxonomy would
need a rule for mixed posts such as "Gym progress and scared to eat," which
discusses both training and eating. Another possible hard boundary is a
personal story that ends by inviting others to share, such as "Anyone else ever
been told 'you dont look like you workout'?"

### Labels

We use the post's main purpose for its final CSV label. Fitness topic (such as
training, nutrition, motivation, or gym culture) goes in the `note` column (it is not a second label).


Eight synthetic boundary cases and their classifications are in
[taxonomy_stress_test.md](taxonomy_stress_test.md).

### `help_request`

**Definition:** The author asks for advice, assessment, or strategies to
address an unresolved problem, choice, or concern in their own fitness life.

**Example 1:** [FBEOD SPLIT](https://www.reddit.com/r/workout/comments/1wh24kx/fbeod_split/)
provides an A/B workout and asks what to change.

**Example 2:** [natural bulk advice](https://www.reddit.com/r/workout/comments/1wh1rfs/natural_bulk_advice/)
asks how to meet the author's calorie and protein goals within food restrictions.

### `discussion_prompt`

**Definition:** The author invites general information, opinions, or other
people's experiences about a fitness topic without seeking advice they can
apply to an unresolved personal concern or choice.

**Example 1:** [What do you listen to when you workout?](https://www.reddit.com/r/workout/comments/1wfqas8/what_do_you_listen_to_when_you_workout/)
asks others about their workout music.

**Example 2:** [What are you working on rn?](https://www.reddit.com/r/workout/comments/1wflemc/what_are_you_working_on_rn/)
asks which once-disliked exercises others now enjoy.

### `sharing`

**Definition:** The author mainly reports an experience or result, states a
view, or offers a recommendation without asking for personal help or inviting
a general exchange.

**Example 1:** [Stronger Than I Thought](https://www.reddit.com/r/workout/comments/1wfpuyc/stronger_than_i_thought/)
celebrates an unexpected bench press result.

**Example 2:** [Machine hammer curl](https://www.reddit.com/r/workout/comments/1wh0wkr/machine_hammer_curl/)
shares excitement about finding a useful machine.

### The hardest boundary

**Which two labels:** `help_request` and `discussion_prompt`.

**Borderline post:** "How do you guys stay off your phone between sets?" (from front-page sample) asks what others do, but the author describes losing
time to their own phone and asks whether a rest timer or airplane mode would
help.

**The decision rule I will use:** Ask what a useful answer would mainly do.
Use `help_request` when it would advise the author about their own unresolved
problem, goal, program, or feeling, including a specific next step or
reassurance, even if the question is phrased as "What do you do?" Use
`discussion_prompt` when it would mainly discuss a fitness topic or describe
the responder's own experience, without telling the author how to address a
personal issue. Personal context alone does not decide the label; when both
kinds of answers seem possible, follow the outcome the author is asking for.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** An AI-assisted importer collected posts from
[r/workout's New feed](https://www.reddit.com/r/workout/new/) on October 3,
2026. It read three paginated Atom feed pages in New order. The first pass
inspected 225 entries to obtain 200 posts, excluding 24 link or crosspost
entries whose full text was not in the r/workout post and one exact-text
duplicate. After I reviewed the CSV, two non-English posts and one repeated
question were replaced with the next three eligible English posts from the
same feed. The replacement posts were selected in feed order, without choosing
their labels. Original text and title-only posts are included; each CSV note
records its source URL and any replacement reason.

**How I labelled them:** I labeled the first 21 posts myself, without AI help;
their notes say `cold`. AI suggested labels for the remaining posts. I read
and confirmed or corrected all 179 suggestions, including the three
replacement posts.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `help_request` | 137 | 68.5% |
| `discussion_prompt` | 44 | 22.0% |
| `sharing` | 19 | 9.5% |
| **Total** | **200** | **100%** |

The 19 `sharing` posts fall below the 30-example target in criterion 3. I kept
the New-feed sample instead of selecting extra posts by label.

**Three hard cases**

**1. [Realisticstrength goals for a 40yo](https://www.reddit.com/r/workout/comments/1ww5wie/realisticstrength_goals_for_a_40yo/) (CSV data row 74)**

> *The post:* A 39-year-old returning to lifting lists his recent strength
> numbers, asks whether larger numbers are realistic, and asks what goals other
> people his age have.
>
> *Could have been:* `discussion_prompt`, because he asks about other people's
> goals, or `help_request`, because he is uncertain what goal to set for his own
> training.
>
> *I chose `help_request`, because:* The general question is tied to an
> unresolved personal choice about realistic strength goals. His age,
> training history, and lifts are context for advice he can use himself.

**2. [I get really lazy when I'm on vacation.](https://www.reddit.com/r/workout/comments/1ww10he/i_get_really_lazy_when_im_on_vacation/) (CSV data row 89)**

> *The post:* The author describes dropping workouts and eating differently
> while traveling, then asks whether the same thing happens to anyone else.
>
> *Could have been:* `sharing`, because most of the post describes the author's
> experience, or `discussion_prompt`, because it invites others to compare
> their experiences.
>
> *I chose `discussion_prompt`, because:* The author says they usually do not
> feel bad about the vacation pattern. A useful answer would describe the
> responder's own vacation habits, not give the author a strategy to change.

**3. [Working out is demoralising man, it feels pointless.](https://www.reddit.com/r/workout/comments/1wux5d5/working_out_is_demoralising_man_it_feels_pointless/) (CSV data row 198)**

> *The post:* After 6–8 weeks of training, the author reports soreness,
> frustration, and no visible progress, but says they plan to keep going.
>
> *Could have been:* `help_request`, because the author has an unresolved
> concern about progress, or `sharing`, because they mainly describe how the
> experience feels.
>
> *I chose `sharing`, because:* The post does not ask for advice, assessment,
> reassurance, or a next step. It reports the author's experience and current
> intention to continue.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`.

**Settings:** 3 epochs, learning rate `2e-5`, batch size 16, maximum input
length 128 tokens, seed 42; the run used a CPU.

**Anything I changed from the defaults, and why:** I set `LABELS` to
`help_request`, `discussion_prompt`, and `sharing` so the notebook matched my
CSV taxonomy. I kept the base model and training settings at their defaults.

**Split sizes:** The notebook's stratified split put 139 posts in training, 31
in validation, and 30 in the held-out test set. The small `sharing` support
means its test F1 will be especially sensitive to individual mistakes.

<!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->

| Label | Train | Validation | Test |
|---|---:|---:|---:|
| `help_request` | 96 | 21 | 20 |
| `discussion_prompt` | 30 | 7 | 7 |
| `sharing` | 13 | 3 | 3 |

The notebook's `train_model()` completed the fine-tuning run and printed
`Trained.` The notebook's `evaluate()` saved held-out metrics in
[results.json](results.json) and the matching posts in
[test_split.csv](test_split.csv). Its saved output was:

```text
accuracy  0.667
macro F1  0.267

  help_request     F1 0.800   (n=20)
  discussion_prompt F1 0.000   (n=7)
  sharing          F1 0.000   (n=3)
```



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* Help obtaining public r/workout posts for `labels.csv`,
  with the first posts left unlabeled for my unaided pass.
- *What came back:* AI suggested Reddit's paginated New Atom feed and wrote
  an importer that gathered 200 source posts with URLs in the CSV notes.
- *What I changed:* I labeled the first 21 posts myself. While reviewing the
  collected posts, I found two non-English posts I had skipped and a repeated
  question. I asked AI to replace those three with the next eligible posts
  from the same feed.
- *How I verified it:* I read the collected posts, checked the replacements,
  and confirmed that `labels.csv` still has 200 distinct posts with source
  URLs.

**Moment 2**

- *What I asked for:* Suggest labels for the remaining posts using my three
  purpose definitions after I finished the unaided pass.
- *What came back:* AI suggested labels for 179 posts, marked them for
  review, flagged difficult cases, and created `review_labels.py` to show each
  full post and let me confirm or change its label.
- *What I changed:* I used the script to read every suggested row and changed
  some labels when another label better matched the kind of answer the post
  invited. For example, I distinguished requests for advice to the author from
  prompts for others to discuss a fitness topic or their own experiences.
- *How I verified it:* The CSV notes distinguish my 21 `cold` labels from the
  179 AI suggestions I checked; none remain marked `review required`.

**Pre-labelling disclosure:** AI suggested labels for 179 of the 200 posts.
I reviewed every suggestion and confirmed or corrected it before training.
The first 21 labels were mine without AI help.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
