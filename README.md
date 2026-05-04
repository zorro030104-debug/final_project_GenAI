# AI Requirement Clarifier

## 1. Context and Problem

In ToB (Business-to-Business) product development, requirements are often vague, incomplete, and expressed as surface-level problems (e.g., “the system is slow”).

Unlike consumer products, stakeholders typically describe **outcomes or symptoms**, rather than structured requirements.
As a result, product managers must interpret and clarify these inputs before they can be used by engineering teams.

This project focuses on an early-stage workflow:

→ Turning vague stakeholder input into structured, actionable requirements

---

## 2. Solution

We built a simple **Streamlit-based GenAI tool** with two modes:

### Baseline

Represents a typical PM quick response:

* informal interpretation
* limited structure
* weak actionability

---

### Improved

Simulates structured product thinking by generating:

* Clarified Requirement
* Assumptions (separated from facts)
* Missing Information
* Clarification Questions
* Internal Checks
* Next Actions
* Risks / Ambiguities

> The goal is not just formatting, but improving **requirement clarity and actionability**.

---

## 3. Why GenAI

This task requires:

* interpreting vague natural language
* reasoning under missing information
* generating structured outputs

Traditional templates are static and context-independent, while GenAI enables **adaptive and context-aware clarification**.

---

## 4. Evaluation

The system is evaluated using 6 realistic requirement inputs across 3 workflow stages:

* After stakeholder request
* Before PRD writing
* Before engineering discussion

### Evaluation Method

Improved outputs are scored using an **8-point checklist**, covering:

* requirement clarity
* assumption separation
* missing information detection
* actionability (questions, next steps)
* risk identification

### Key Results

* Improved outputs consistently achieved **high scores (7–8 / 8)**
* Baseline outputs were:

  * less structured
  * less complete
  * less actionable

More importantly, improvements were observed in:

* handling ambiguous input
* decomposing multi-intent requirements
* identifying missing context
* enabling concrete next steps

👉 Full evaluation details: see `evaluation.md`

---

## 5. Limitations

* Outputs may still be generic in complex domains
* Domain-specific knowledge is not always captured
* The system depends on input quality
* Human validation is still required

---

## 6. Use Case

This tool can be used in early-stage ToB workflows:

* after receiving stakeholder input
* before writing PRD
* before discussing with engineering

It helps product managers:

* clarify vague requirements
* identify missing information
* prepare for stakeholder alignment

---

## 7. Notes on Data

The test inputs are **synthetic**, but designed to reflect realistic stakeholder communication patterns.

Stakeholders typically express:

* problems rather than requirements
* incomplete or ambiguous information

This is supported by prior work in product management and requirements engineering
(Cagan, 2018; Wiegers & Beatty, 2013).

Because real ToB requirements are often confidential, synthetic inputs are used to simulate realistic scenarios.

---

## 8. References

Cagan, M. (2018). *Inspired: How to create tech products customers love* (2nd ed.). Silicon Valley Product Group.

Wiegers, K. E., & Beatty, J. (2013). *Software requirements* (3rd ed.). Microsoft Press.

---

## 9. How to Run

```bash
pip install streamlit openai
streamlit run app.py
```

Then open: http://localhost:8501
