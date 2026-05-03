# AI Requirement Clarifier

## 1. Context and Problem

In business (especially enterprise / ToB) product development, requirements are often vague, incomplete, and unstructured.
This leads to misalignment, repeated clarification, and delays.

This project focuses on a narrow workflow:

→ Turning vague requirements into structured, actionable specifications

---

## 2. Solution

We built a simple Streamlit-based GenAI tool with two modes:

**Baseline (status quo):**
Represents a typical real-world workflow where a product manager informally summarizes a requirement without structured guidance.

**Improved (GenAI structured output):**
The system generates:

* Clarified Requirement
* Missing Information
* Clarification Questions
* Risks / Ambiguities

The key idea is that **prompt design enables structured reasoning**, not just summarization.

---

## 3. Why GenAI

This task requires:

* interpreting vague natural language
* identifying missing information
* generating structured outputs

Traditional rule-based systems or templates cannot reliably handle this variability.

---

## 4. Evaluation Summary

We tested the system on 8 realistic requirement inputs (see `input.txt`), inspired by public sources such as GitHub feature requests and product feedback.

### Evaluation Criteria

Outputs are evaluated based on:

* **Clarity** (is the requirement clearer?)
* **Completeness** (are missing elements identified?)
* **Actionability** (can a product team act on it?)

### Key Result

| Aspect                 | Baseline (Manual-style summary) | Improved (Structured) |
| ---------------------- | ------------------------------- | --------------------- |
| Structure              | ×                               | √                     |
| Missing info detection | ×                               | √                     |
| Actionability          | ×                               | √                     |
| Handling vague input   | ⚠                              | √                     |

**Conclusion:**
The structured GenAI approach significantly improves requirement clarity and usability compared to typical informal workflows.

- Detailed case-by-case comparison: see `evaluation.md`
- Example outputs: see `/output`

---

## 5. Limitations

* Outputs can still be somewhat generic
* Domain-specific constraints may be missing
* The system relies on input quality
* **Human review is still required**, especially for complex or regulated domains

The system may perform poorly when:

* requirements contain hidden business rules
* domain expertise is required but not stated

---

## 6. How to Run

```bash
pip install streamlit openai
streamlit run app.py
```

Open in browser(not recommended):
http://localhost:8501

---

## 7. Project Structure

project/
├── app.py
├── input.txt
├── evaluation.md
├── output/
│   ├── #1-baseline.png
│   ├── #1-improved.png
│   └── ...

---

## 8. Notes on Data

The test inputs are synthetic but designed to reflect realistic patterns observed in public sources (e.g., GitHub feature requests, product feedback).

Due to the private nature of real product requirements, synthetic data is used to simulate real-world scenarios.

---

## 9. Use Case

This tool can be used as a lightweight assistant in early-stage product workflows to:

* identify missing requirement details
* prepare for stakeholder discussions
* reduce ambiguity before specification writing
