# Daily Reflection Tree

A deterministic end-of-day reflection tool built as a structured decision tree. No LLM is called at runtime. The tree is the product.

---

## Repository Structure

```
/tree/
  reflection-tree.json     ← The full decision tree (35+ nodes, all 3 axes)
  tree-diagram.md          ← Visual Mermaid diagram of the tree structure

/agent/
  agent.py                 ← CLI agent that walks the tree (Part B)

/transcripts/
  persona-1-transcript.md  ← "Victim / Entitled / Self-Centric" path walkthrough
  persona-2-transcript.md  ← "Victor / Contributing / Altrocentric" path walkthrough

write-up.md                ← Design rationale and psychological grounding
README.md                  ← This file
```

---

## Part A: Reading the Tree

Open `tree/reflection-tree.json`. Each node has:

| Field | Meaning |
|-------|---------|
| `id` | Unique node identifier |
| `parentId` | Parent node (builds the hierarchy) |
| `type` | `start`, `question`, `decision`, `reflection`, `bridge`, `summary`, `end` |
| `text` | What the employee sees. `{NODE_ID.answer}` placeholders get substituted. |
| `options` | For questions: fixed choices. For decisions: routing rules (`answer=X\|Y:TARGET_ID`). |
| `target` | Explicit jump target (overrides child lookup). |
| `signal` | Tally tag recorded in state. e.g. `axis1:internal` |

### Tracing a Path (No Code Needed)

1. Start at node `id: "START"`
2. Follow `target` or find the child node with `parentId` matching the current node's `id`
3. At `question` nodes, pick an option — this sets `last_answer`
4. At `decision` nodes, match `last_answer` against routing rules to find the next node
5. `signal` tags accumulate in state and determine the final SUMMARY text

### Tree Stats

| Metric | Count | Requirement |
|--------|-------|-------------|
| Total nodes | 35+ | 25+ ✅ |
| Question nodes | 10+ | 8+ ✅ |
| Decision nodes | 8+ | 4+ ✅ |
| Reflection nodes | 6 | 4+ ✅ |
| Bridge nodes | 2 | 2+ ✅ |
| Axes covered | 3 | All 3 ✅ |
| Summary node | 1 | 1+ ✅ |

---

## Part B: Running the Agent

**Requirements:** Python 3.10+, no external libraries needed.

```bash
# From the repo root:
python agent/agent.py

# Or specify a custom tree file:
python agent/agent.py --tree path/to/reflection-tree.json
```

The agent:
- Validates the full tree on startup (guardrail against malformed data)
- Walks node-by-node, displaying text and collecting fixed-choice answers
- Branches deterministically based on answers — no randomness, no LLM
- Interpolates reflection text with the employee's earlier answers
- Produces a personalized summary from 8 possible templates based on the 3-axis outcome

---

## Design Principles

1. **No LLM at runtime.** The agent is pure Python with no API calls.
2. **Deterministic.** Same answers → same path → same reflection. Every time.
3. **Fixed options only.** No free text input. Every question has 3–5 choices.
4. **Anti-hallucination guardrails.** The agent validates all node references and routing rules before execution. Missing nodes, broken routes, and infinite loops all raise descriptive errors rather than silently misbehaving.
5. **No moralizing.** Reflection text acknowledges both poles without shaming.

---

## Psychological Foundations

| Axis | Framework | Source |
|------|-----------|--------|
| Locus (Victim vs Victor) | Locus of Control | Rotter (1954); Dweck (2006) |
| Orientation (Entitlement vs Contribution) | Psychological Entitlement / OCB | Campbell et al. (2004); Organ (1988) |
| Radius (Self vs Altrocentric) | Self-Transcendence / Perspective-Taking | Maslow (1969); Batson (2011) |
