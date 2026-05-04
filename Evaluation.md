# Evaluation

## 1. Evaluation Goal

This evaluation tests whether the Improved mode provides more structured and actionable requirement clarification compared to the Baseline mode.

---

## 2. Evaluation Criteria (Improved)

| Criterion               | Description             | Score |
| ----------------------- | ----------------------- | ----- |
| Surface Requirement     | Correct restatement     | 0/1   |
| Assumptions             | Clearly separated       | 0/1   |
| Clarified Requirement   | More actionable rewrite | 0/1   |
| Missing Information     | ≥ 3 items               | 0/1   |
| Clarification Questions | ≥ 3 questions           | 0/1   |
| Internal Checks         | ≥ 2 checks              | 0/1   |
| Next Actions            | ≥ 2 actions             | 0/1   |
| Risks / Ambiguities     | ≥ 2 risks               | 0/1   |

---

## 3. Results Summary

Across all cases, the Improved mode consistently outperforms the Baseline mode in:

| Aspect                 | Baseline      | Improved               |
| ---------------------- | ------------- | ---------------------- |
| Structure              | Informal      | Clearly structured     |
| Missing info detection | Rare          | Consistent             |
| Actionability          | Weak          | Strong                 |
| Handling ambiguity     | Poor          | Effective              |
| Multi-intent handling  | Not supported | Explicit decomposition |

All Improved outputs achieved high scores (7–8), indicating strong consistency.

---

## 4. Case Analysis (Key Differences)

### Case 1 — Dashboard unclear

**Key challenge:** unclear metrics / stakeholder intent

* Baseline: treats it as a general UI issue
* Improved: identifies missing metric definitions and user roles

-> Improvement: moves from UI-level thinking to **data + user context clarification**

---

### Case 2 — User activity tracking

**Key challenge:** undefined tracking scope

* Baseline: suggests tracking behavior
* Improved: distinguishes between analytics goals (monitoring vs decision-making)

-> Improvement: introduces **use-case differentiation**

---

### Case 3 — Checkout slow/confusing

**Key challenge:** performance vs UX ambiguity

* Baseline: general performance suggestion
* Improved: separates possible causes (system, UX, network)

-> Improvement: adds **cause-level reasoning instead of surface fix**

---

### Case 4 — Manual reporting

**Key challenge:** workflow inefficiency

* Baseline: suggests automation
* Improved: identifies process bottlenecks and missing system integration

-> Improvement: shifts from solution suggestion to **workflow diagnosis**

---

### Case 5 — "Make it better"

**Key challenge:** extreme ambiguity

* Baseline: almost unusable
* Improved: converts vague input into structured clarification questions

-> Improvement: demonstrates ability to handle **low-information input**

---

### Case 6 — Multi-intent requirement

**Key challenge:** multiple goals in one request

* Baseline: treats as single requirement
* Improved: splits into dashboard + reporting components

-> Improvement: enables **requirement decomposition**

---

## 5. Key Findings

* Baseline outputs are limited to quick interpretations
* Improved outputs provide structured reasoning and actionable steps
* The biggest gain is in:

  * handling ambiguity
  * identifying missing information
  * enabling next actions

---

## 6. Conclusion

The results show that:

> The improvement is not only structural, but reflects a more advanced and systematic product thinking process.

---

## 7. Notes

* Full outputs are available in `/output`
* Scores are checklist-based and support comparison, not replace human judgment
