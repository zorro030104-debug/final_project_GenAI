# Evaluation Details

---

## 1. Test Setup

To evaluate the effectiveness of the system, we constructed a test set of 8 representative requirement inputs (see `input.txt`). These inputs cover a range of real-world scenarios in ToB product workflows:

* Clear but incomplete requirements
* Moderately vague requirements
* UX improvement requests
* Workflow optimization scenarios
* Extremely vague inputs (edge cases)
* Multi-intent requirements
* Ambiguous business goals

This diversity ensures that the system is tested across different levels of ambiguity and complexity.

---

## 2. Evaluation Criteria

The evaluation follows the rubric defined in the project design:

* **Clarity:** Does the output improve understanding of the requirement?
* **Completeness:** Does it identify missing information?
* **Hallucination Control:** Does it avoid inventing unsupported details?
* **Structure:** Does it follow a consistent format?
* **Usefulness:** Are the outputs actionable and relevant?

---

## 3. Case-Based Comparison

Below are selected examples demonstrating differences between the **Baseline** and **Improved** approaches.

---

### Case 1: Sales Dashboard Requirement

**Input:**

> We need a dashboard for sales performance

**Baseline Output:**

* Provides a general summary of a sales dashboard
* Mentions metrics and insights at a high level
* Lacks structure and does not identify missing details

**Improved Output:**

* Rewrites the requirement with clearer scope (metrics, trends, categories)
* Identifies missing information such as:

  * target users
  * data sources
  * update frequency
* Generates relevant clarification questions
* Highlights risks such as unclear metrics and audience

**Key Insight:**
The improved version converts a descriptive statement into a structured and actionable requirement.

---

### Case 2: User Activity Tracking

**Input:**

> Build something to track user activity

**Baseline Output:**

* Produces a high-level description of tracking user behavior
* Remains generic and descriptive

**Improved Output:**

* Specifies concrete tracked events (logins, page views, interactions)
* Identifies missing elements:

  * purpose of tracking
  * privacy constraints
  * system scale
* Raises practical implementation questions
* Identifies risks such as data privacy concerns

**Key Insight:**
The improved version moves from vague description to implementation-aware clarification.

---

### Case 3: Checkout Experience Improvement

**Input:**

> Improve the checkout experience

**Baseline Output:**

* Suggests general improvements (usability, efficiency)
* Remains abstract

**Improved Output:**

* Reframes the requirement into measurable goals (reduce friction, improve conversion)
* Identifies missing information:

  * success metrics
  * user segments
  * existing pain points
* Generates actionable clarification questions
* Highlights risks such as focusing on the wrong UX aspects

**Key Insight:**
The improved version connects the requirement to measurable outcomes.

---

### Case 4: Reporting Improvement

**Input:**

> Make reporting easier

**Baseline Output:**

* Describes simplifying reporting processes
* Lacks specificity

**Improved Output:**

* Specifies improvements (automation, report generation, sharing)
* Identifies missing details:

  * report types
  * user roles
  * integration requirements
* Raises targeted clarification questions
* Highlights risks such as misalignment with user needs

**Key Insight:**
The improved version introduces structure and stakeholder awareness.

---

### Case 5: Approval Workflows

**Input:**

> We want better approval workflows

**Baseline Output:**

* Focuses on improving efficiency
* Does not analyze workflow complexity

**Improved Output:**

* Clarifies goals (reduce processing time, improve user experience)
* Identifies missing workflow details:

  * stakeholders
  * workflow types
  * performance metrics
* Raises detailed questions
* Identifies risks such as organizational resistance

**Key Insight:**
The improved version captures organizational and process complexity.

---

### Case 6: Extremely Vague Input

**Input:**

> Make it better

**Baseline Output:**

* Produces a generic improvement statement
* Does not acknowledge ambiguity

**Improved Output:**

* Explicitly identifies the requirement as vague
* Lists multiple missing dimensions:

  * scope
  * users
  * metrics
* Raises critical clarification questions
* Flags risks such as subjective interpretation and scope creep

**Key Insight:**
The improved version handles ambiguity explicitly, while the baseline fails to recognize it.

---

### Case 7: Multi-Intent Requirement

**Input:**

> Build a dashboard and improve reporting for management

**Baseline Output:**

* Combines both ideas into a general description
* Does not separate concerns

**Improved Output:**

* Breaks down the requirement into dashboard and reporting components
* Identifies missing details for both aspects
* Raises questions about scope, KPIs, and priorities
* Highlights risks such as unclear prioritization

**Key Insight:**
The improved version reveals hidden complexity in multi-intent inputs.

---

### Case 8: Internal Productivity Optimization

**Input:**

> Optimize our internal tools for better productivity

**Baseline Output:**

* Describes general productivity improvement
* Remains abstract

**Improved Output:**

* Reframes into efficiency and user experience goals
* Identifies missing information:

  * tools involved
  * target users
  * performance metrics
* Raises actionable questions
* Highlights risks such as unclear measurement

**Key Insight:**
The improved version connects vague goals to measurable dimensions.

---

## 4. Overall Findings

Across all test cases, the following patterns were observed:

* The baseline approach produces general summaries but lacks actionable value
* The improved approach consistently produces structured outputs
* Missing information is systematically identified in the improved version
* Clarification questions significantly improve requirement quality
* The improved system handles vague and ambiguous inputs more effectively

---

## 5. Limitations Observed

During testing, several limitations were identified:

* Some clarification questions are repetitive or generic
* Domain-specific constraints may be missing
* Outputs depend on prompt quality and may vary
* Multi-intent requirements may still require human interpretation

---

## 6. Conclusion

The evaluation demonstrates that **prompt design plays a critical role in improving GenAI workflow performance**.

Compared to a simple baseline, the structured prompt:

* Improves clarity and completeness
* Reduces ambiguity
* Produces more actionable outputs

However, human involvement remains necessary to ensure correctness and alignment with business needs.

---
