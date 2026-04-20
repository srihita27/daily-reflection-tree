# Write-Up: Daily Reflection Tree — Design Rationale

## Why These Questions?

The three axes (Locus, Orientation, Radius) describe a psychological progression — and the questions were designed to surface each without moralizing.

**Axis 1 (Locus of Control)** starts with a deliberately low-stakes opener: "describe today in one word." This is a warm-up, not a data point — it creates trust and gives the tree a branching handle. The second and third questions probe attribution. The key design decision was to use concrete behavioral options ("I adapted," "I waited," "I felt stuck") rather than abstract statements ("I believe I control my destiny"). Rotter's original LOC Scale used self-report beliefs; in a tired employee at 7pm, behavioral recall is more honest than belief-endorsement.

**Axis 2 (Contribution vs Entitlement)** was the hardest to design without moralizing. Options like "I felt I deserved more recognition" are uncomfortable to choose — people avoid them. The solution was to make them *specific* and *normalized*: "I felt I deserved more recognition for my work" sounds like something a real person would think, not a confession. Campbell et al. (2004) note that entitlement is invisible to the person holding it — the tree's job is to make it visible without triggering defensiveness. That required options that are honest but not accusatory.

**Axis 3 (Radius)** uses a progression from narrow to wide: Just me → My team → A specific colleague → The people we serve. This was inspired directly by Batson's (2011) perspective-taking literature — the capacity to widen concern is a skill, and the tree scaffolds it by naming the levels.

## Branching Design: Trade-offs

The tree uses **two-stage branching per axis**: an opening question creates a high/low split, then a second question refines within that half. This avoids a flat "which pole are you?" question and creates the feeling of a conversation.

The main trade-off: two-stage branching multiplies paths, increasing tree size. With 3 axes × 2 stages × 2 poles, the theoretical minimum is 8 terminal paths. The tree manages this by **merging mid-axis** — after the second question on each axis, all paths converge to two reflection nodes (internal/external, contribution/entitlement, altrocentric/self). This keeps the tree tractable while preserving per-person specificity.

Decision nodes are invisible to the user — they are pure routing machinery, not a user experience. This separates *data collection* (question nodes) from *logic* (decision nodes), making the tree readable as data independent of any agent code.

## Psychological Sources

- **Rotter, J.B. (1954).** Social learning and clinical psychology. — Foundational LOC framework; Rotter's scale informed the distinction between "I adapted" vs "I waited."
- **Dweck, C. (2006).** Mindset: The New Psychology of Success. — Growth mindset shapes Axis 1 reflection text: "you stayed curious about the parts that were in your control."
- **Campbell, W.K. et al. (2004).** — Psychological Entitlement: Interpersonal Consequences and Validation of a Self-Report Measure. — Informed Axis 2 option design; entitlement is dispositional, not situational, so options must bypass defensiveness.
- **Organ, D.W. (1988).** Organizational Citizenship Behavior. — Discretionary effort beyond formal role = contribution orientation. Axis 2 reflection text references this explicitly.
- **Maslow, A. (1969).** The Farther Reaches of Human Nature. — Self-transcendence as the peak beyond self-actualization. Axis 3 reflection text quotes the concept directly.
- **Batson, C.D. (2011).** Altruism in Humans. — Perspective-taking as a cognitive skill; the Axis 3 option progression (self → team → colleague → customer) operationalizes this gradient.

## What I'd Improve With More Time

**1. More axis-crossing.** The current tree moves linearly through axes. A stronger design would let Axis 2 reference Axis 1 signals: "You said you adapted when things shifted — did you notice an opportunity to give something in that adaptation?" The psychological literature supports this: agency and contribution are deeply linked.

**2. Longitudinal state.** A single session can't change mindset. A stronger product would track signals across 30 days and show the employee their trend: "This week you leaned more external than usual — what's different?" This requires session persistence but no LLM.

**3. Question-by-question A/B testing.** Some of the options I designed may not cleanly separate the poles in practice — a real person might answer "I pushed through alone" and mean it as either internal *or* external depending on context. Iterating with real users and analysing path distributions would sharpen the options considerably.

**4. A "recalibration" branch.** For employees who answer every question at the extreme (all internal, all contribution, all altrocentric), a gentle pushback branch would add depth: "You described yourself as fully in control today. Was there anything outside your control that you haven't fully acknowledged?"
