# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Held-out accuracy

The fine-tuned model reaches at least 0.75 accuracy on the held-out test split
in each of the three seed runs.

**Why this target:** r/workout mixes personal routine and nutrition help
requests, general gym discussion prompts, and progress or anecdote posts, so I
want TakeMeter to sort these three purposes correctly more than 70% of the
time. With about 30 held-out posts, 0.75 requires at least 23 correct in every
run and exceeds the largest label share allowed by the assignment.

---

## 2. F1 floor for every label

Each of `help_request`, `discussion_prompt`, and `sharing` reaches an F1 score
of at least 0.60 on the held-out test split in each of the three seed runs.

**Why this target:** A post asking how to stay off a phone between sets could
look like a general discussion prompt but seeks help with the author's own
problem (overall accuracy could hide repeated mistakes at this boundary). If a
label has only 30 of the 200 posts, roughly 4 or 5 will reach a 15% test split,
so 0.60 F1 is a meaningful floor without demanding near-perfect scores from
such a small group.

---

## 3. Enough examples of every label

In `labels.csv`, each of `help_request`, `discussion_prompt`, and `sharing`
appears at least 30 times, and no label accounts for more than 70% of rows.

**Why this target:** The r/workout posts we read include personal help requests,
general workout discussions, and progress or gym-experience shares, but these
purposes need not occur equally often. Thirty examples gives even the least
common purpose some training data, while the 70% cap limits majority-label
guessing. I will report a missed target rather than select posts to force it.

---

## 4. Repeatable labeling

On a blind second labeling of 30 posts sampled from `labels.csv` with
`pandas.DataFrame.sample(n=30, random_state=42)`, at least 24 second-pass labels
match the original labels.

**Why this target:** The gym-guilt and phone-distraction examples show that a
"what do you do?" question can be a personal help request, so I need to make
the same call when I see similar r/workout posts again. A 24/30 match allows
six hard cases to differ while revealing whether I apply the
`help_request`/`discussion_prompt` rule consistently.

---

## 5. Limit confusion at the hardest boundary

In each of the three seed runs, no more than 25% of held-out posts whose true
label is `help_request` or `discussion_prompt` are predicted as the other of
those two labels. Divide the number of these two cross-label errors by the
combined held-out support for the two labels.

**Why this target:** An r/workout post asking how others stay off their phones
between sets could look like a general discussion prompt, but its author is
seeking help with a personal problem. This is the hardest boundary in my
taxonomy, so I want at least three quarters of posts at that boundary to
avoid this specific mix-up across all three test splits.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
