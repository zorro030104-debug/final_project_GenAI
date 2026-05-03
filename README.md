# AI Requirement Clarifier for ToB Product Workflows

## 1. Context and Problem

### What is ToB (Business-to-Business)

ToB (Business-to-Business) refers to products or services designed for organizations rather than individual consumers. Compared to ToC (Business-to-Consumer) products, ToB workflows typically involve multiple stakeholders, more complex processes, and less clearly defined requirements.

As a result, requirements in ToB environments are often expressed in vague or incomplete ways, making early-stage clarification particularly important.

### Background

In ToB product development, requirements are often vague and unstructured, leading to misalignment, delays, and rework.

This project focuses on improving the requirement clarification workflow by transforming vague inputs into structured and actionable outputs.

### Target User and Workflow

This tool is designed for:

* Product Managers
* Business Analysts

Workflow:

* Input: a vague or incomplete requirement
* Output: a structured clarification including missing information and follow-up questions

---

## 2. Solution

We built a Streamlit-based GenAI application with two modes:

Baseline:

* Uses a simple prompt to summarize the requirement
* Produces a short, unstructured output

Improved:

* Uses a structured prompt to generate:

  * Clarified Requirement
  * Missing Information
  * Clarification Questions
  * Risks / Ambiguities

The key idea is that better prompt design leads to more useful outputs.

---

## 3. Why GenAI

This task requires:

* interpreting vague natural language
* identifying missing information
* generating structured outputs

Traditional rule-based methods cannot handle this variability effectively, while LLMs can generalize across different requirement scenarios.

---

## 4. Evaluation Summary

We tested the system on 8 representative inputs (see `input.txt`), including:

* incomplete requirements
* vague inputs
* workflow and UX improvements
* extreme ambiguity cases

### Key Results

Baseline vs Improved:

* Structured Output: Baseline ❌ | Improved ✔
* Missing Information Detection: Baseline ❌ | Improved ✔
* Clarification Questions: Baseline ❌ | Improved ✔
* Handling Vague Input: Baseline ⚠️ | Improved ✔

Conclusion:
The improved version produces more structured and actionable outputs and handles ambiguity significantly better than the baseline.

📄 Detailed case analysis: see `evaluation.md`

---

## 5. Limitations

* Some outputs are generic or repetitive
* Domain-specific constraints may be missing
* Outputs depend on prompt design
* Human review is still required before using results in real workflows

---

## 6. How to Run

Install dependencies:

pip install streamlit openai

Run the app:

streamlit run app.py

Then open:

http://localhost:8501

---

## 7. Project Structure

FINAL_PROJECT_GENAI/
├── app.py
├── input.txt
├── evaluation.md
├── output/
│   ├── #1-baseline.png
│   ├── #1-improved.png
│   └── ...

---

## 8. Artifact

See the `output/` folder for example results.

---

## 9. Conclusion

This project demonstrates that structured prompt design significantly improves the usefulness of GenAI in requirement clarification workflows.

Compared to a simple baseline, the improved approach produces more actionable, structured, and context-aware outputs, especially for vague or ambiguous inputs.

Human-in-the-loop validation remains necessary for real-world deployment.
