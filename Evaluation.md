# Evaluation

## 1. Overview

This evaluation compares two versions of the AI Requirement Clarifier:

**Baseline:**
A simple summary output that represents a common informal workflow, where a vague requirement is briefly restated without structured analysis.

**Improved:**
A structured GenAI output that clarifies the requirement and organizes the response into:

* Clarified Requirement
* Missing Information
* Clarification Questions
* Risks / Ambiguities

The evaluation uses 8 realistic ToB-style requirement inputs from `input.txt`.

---

## 2. Evaluation Criteria

The outputs are evaluated based on three criteria:

1. **Clarity**
   Does the output make the original requirement easier to understand?

2. **Completeness**
   Does the output identify missing users, goals, data, constraints, scope, success metrics, or timeline?

3. **Actionability**
   Does the output help a product manager or business analyst know what to ask or do next?

---

## 3. Case-by-Case Evaluation

### Case 1: Dashboard for System Performance

**Input:**
Users have requested a dashboard to monitor system performance and metrics in a more structured way.

**Baseline Result:**
The baseline summarizes the need for a dashboard and explains that it would help users monitor system data. However, it does not identify what metrics should be shown, who the dashboard is for, or what data sources are needed.

**Improved Result:**
The improved version clarifies the dashboard purpose and identifies missing information such as users, goals, data sources, constraints, scope, success metrics, and timeline. It also asks specific questions about dashboard users, key metrics, update frequency, and success measurement.

**Finding:**
The improved version is more useful because it turns a general dashboard request into a structured planning document.

---

### Case 2: User Activity Tracking

**Input:**
The product team wants a way to track user activity across the platform.

**Baseline Result:**
The baseline gives a general summary of tracking user behavior and improving user experience. It remains high-level and does not surface technical, privacy, or measurement questions.

**Improved Result:**
The improved version clarifies that the system should monitor and log user activity. It identifies missing information about users, goals, data, legal/privacy constraints, scope, success metrics, and timeline. It also raises important risks such as privacy, scope creep, data overload, and implementation feasibility.

**Finding:**
The improved version performs better because activity tracking requires careful definition of data, users, privacy requirements, and success metrics.

---

### Case 3: Checkout Experience Improvement

**Input:**
Users report that the checkout process is slow and confusing, and it needs improvement.

**Baseline Result:**
The baseline summarizes the checkout issue and states that improvements should increase user satisfaction and efficiency. However, it does not ask what part of checkout is slow or how success should be measured.

**Improved Result:**
The improved version clarifies the goal of improving checkout speed and user experience. It identifies missing information about affected users, desired improvements, data, constraints, scope, success metrics, and timeline. It also highlights risks such as weak user feedback validation, scope creep, technical feasibility, unclear success measurement, and user segmentation.

**Finding:**
The improved version is more actionable because it connects the UX problem to measurable outcomes such as checkout time, conversion rate, and user satisfaction.

---

### Case 4: Manual Reporting Process

**Input:**
The operations team struggles with manual reporting and wants to simplify the reporting process.

**Baseline Result:**
The baseline summarizes the reporting problem and says the team wants to streamline reporting to reduce time and effort. It does not identify what reports are involved, who uses them, or what data sources are required.

**Improved Result:**
The improved version clarifies that the operations team needs a solution to automate and simplify reporting. It identifies missing information about users, goals, data, constraints, scope, success metrics, and timeline. It also asks about current reporting challenges, report examples, critical reports, existing tools, and measurement criteria.

**Finding:**
The improved version is stronger because it reveals the operational details needed before designing a reporting solution.

---

### Case 5: Expense Approval Workflow

**Input:**
The finance team wants better approval workflows for expense requests.

**Baseline Result:**
The baseline explains that the finance team wants to improve efficiency and tracking of expense approvals. However, it does not identify workflow steps, stakeholders, compliance needs, or approval metrics.

**Improved Result:**
The improved version clarifies the need for an improved approval workflow for processing expense requests. It identifies missing information about users, goals, data, constraints, scope, success metrics, and timeline. It also raises risks such as user resistance, integration challenges, unclear assumptions, scope creep, and the need for human review.

**Finding:**
The improved version is more appropriate for enterprise workflows because approval processes often involve multiple stakeholders, compliance constraints, and system integrations.

---

### Case 6: Extremely Vague Requirement

**Input:**
A stakeholder simply said: make it better.

**Baseline Result:**
The baseline produces a generic statement about improving an unspecified area or project. It does not recognize how vague the requirement is or explain what information is missing.

**Improved Result:**
The improved version creates a tentative clarification but also identifies that key information is missing. It asks about target users, improvement goals, metrics, constraints, scope, success measurement, and timeline. It also flags risks such as unclear goals, subjective interpretation of “better,” scope creep, and the need for user feedback.

**Finding:**
This is the clearest example of the improved system’s value. The baseline treats the input as if it is usable, while the improved version exposes the ambiguity and turns it into follow-up questions.

---

### Case 7: Dashboard and Reporting for Decision-Making

**Input:**
Management wants a dashboard and improved reporting for decision-making.

**Baseline Result:**
The baseline summarizes the need for a dashboard with enhanced reporting. It does not separate the dashboard requirement from the reporting requirement or identify priority, users, data, or success metrics.

**Improved Result:**
The improved version clarifies that management needs dashboard and reporting capabilities to support data-driven decision-making. It identifies missing users, goals, data sources, constraints, scope, success metrics, and timeline. It also asks questions about decisions to support, data sources, dashboard features, budget, and delivery timeline.

**Finding:**
The improved version handles the multi-intent requirement better by exposing hidden complexity around dashboard design, reporting depth, and management decision needs.

---

### Case 8: Internal Tools Optimization

**Input:**
The company wants to optimize internal tools to improve employee productivity.

**Baseline Result:**
The baseline summarizes the goal of improving productivity by optimizing internal tools. It remains broad and does not specify which tools, users, or productivity measures are involved.

**Improved Result:**
The improved version clarifies the goal of improving efficiency through internal tool optimization. It identifies missing information about employee groups, goals, data, constraints, scope, success metrics, and timeline. It also asks about specific tools, current pain points, productivity measurements, budget, technological constraints, and reassessment frequency.

**Finding:**
The improved version is more useful because productivity improvement is broad and must be connected to specific tools, user groups, and measurable outcomes.

---

## 4. Overall Findings

Across all 8 test cases, the improved version consistently produced more useful outputs than the baseline.

The baseline usually:

* Restated the requirement
* Added a general business goal
* Did not identify missing details
* Did not provide structured next steps

The improved version consistently:

* Clarified the requirement
* Identified missing information
* Asked relevant follow-up questions
* Highlighted risks and ambiguity
* Helped prepare for stakeholder discussion

---

## 5. Summary Comparison

| Evaluation Area     | Baseline                   | Improved                                                                 |
| ------------------- | -------------------------- | ------------------------------------------------------------------------ |
| Clarity             | Provides a general summary | Rewrites the requirement more clearly                                    |
| Completeness        | Usually misses key gaps    | Identifies users, goals, data, constraints, scope, metrics, and timeline |
| Actionability       | Limited next-step value    | Provides concrete questions and risks                                    |
| Ambiguity Handling  | Weak                       | Strong, especially in Case 6                                             |
| Business Usefulness | Low to moderate            | High for early-stage requirement clarification                           |

---

## 6. Limitations Observed

The improved system is more useful than the baseline, but it still has limitations:

* Some questions are somewhat generic across cases.
* The model may assume common business structures when details are missing.
* Domain-specific rules, compliance requirements, or technical constraints may still be missed.
* Human review is required before using the output as a final requirement document.

---

## 7. Conclusion

The evaluation shows that the structured GenAI approach provides clear improvement over a simple baseline summary.

The main value of the improved system is not just generating text, but helping product managers and business analysts think through missing information, stakeholder questions, and project risks.

This makes the tool useful as an early-stage requirement clarification assistant, while still requiring human judgment for final decisions.
