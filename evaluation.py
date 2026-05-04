import os
import csv
import re
from openai import OpenAI

client = OpenAI()

INPUT_FILE = "input.txt"
OUTPUT_FILE = "evaluation_results.csv"

WORKFLOW_STAGES = [
    "After stakeholder request",
    "Before PRD writing",
    "Before engineering discussion"
]


def read_inputs(file_path):
    """
    Reads input.txt and extracts requirement examples.
    Lines starting with # are ignored.
    Empty lines are ignored.
    """
    inputs = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                inputs.append(line)

    return inputs


def baseline_response(text, stage):
    prompt = f"""
You are a product manager receiving a vague stakeholder request.

Provide a quick informal PM analysis.

### Initial Understanding
Explain what the stakeholder may mean.

### Possible Cause or Scenario
Give 1-2 possible interpretations based on experience.

### Quick Suggestion
Give a high-level suggestion for what the team might do next.

Requirement:
{text}

Workflow stage:
{stage}

Rules:
- Keep it short.
- This is an informal quick take, not a structured requirement clarification.
- You may make reasonable assumptions, but do not deeply validate them.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response.choices[0].message.content


def improved_response(text, stage):
    prompt = f"""
You are a ToB product manager working at the early stage of requirement clarification.

Stakeholder inputs are often vague, incomplete, and symptom-based.
Your task is to simulate structured product thinking before writing a PRD or assigning development work.

Given the requirement below, provide a structured PM clarification.

### 1. Surface Requirement
Restate exactly what the stakeholder said, without adding new facts.

### 2. Assumptions
List reasonable assumptions about users, scenarios, or possible causes.
Clearly mark them as assumptions, not facts.

### 3. Clarified Requirement Draft
Rewrite the requirement in a clearer, more actionable form.
Do not invent metrics, technical solutions, or business rules.

### 4. Missing Information
List key missing details, such as user type, context, scope, constraints, success criteria, and priority.

### 5. Clarification Questions
List concrete questions the PM should ask the stakeholder.

### 6. Internal Checks
List what the PM should check with internal teams, such as engineering, data, operations, or support.

### 7. Next Actions
Suggest practical next steps before development.

### 8. Risks / Ambiguities
Identify possible misunderstandings, hidden business rules, scope creep, and areas requiring human review.

Requirement:
{text}

Workflow stage:
{stage}

Rules:
- Do not invent facts.
- Separate confirmed information from assumptions.
- Focus on early-stage ToB product workflows.
- Be concise and practical.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


def count_bullets(section_text):
    """
    Counts bullet-like lines in a section.
    """
    lines = section_text.splitlines()
    count = 0

    for line in lines:
        line = line.strip()
        if line.startswith("-") or line.startswith("*") or re.match(r"^\d+[\.\)]", line):
            count += 1

    return count


def extract_section(text, section_name):
    """
    Extracts a section based on markdown heading.
    """
    pattern = rf"###.*{re.escape(section_name)}.*?(?=###|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(0)

    return ""


def evaluate_improved_output(output):
    """
    Evaluates Improved output using an 8-point checklist.
    """
    score = 0

    surface = extract_section(output, "Surface Requirement")
    assumptions = extract_section(output, "Assumptions")
    clarified = extract_section(output, "Clarified Requirement")
    missing = extract_section(output, "Missing Information")
    questions = extract_section(output, "Clarification Questions")
    internal = extract_section(output, "Internal Checks")
    actions = extract_section(output, "Next Actions")
    risks = extract_section(output, "Risks")

    if surface.strip():
        score += 1

    if assumptions.strip():
        score += 1

    if clarified.strip():
        score += 1

    if count_bullets(missing) >= 3:
        score += 1

    if count_bullets(questions) >= 3:
        score += 1

    if count_bullets(internal) >= 2:
        score += 1

    if count_bullets(actions) >= 2:
        score += 1

    if count_bullets(risks) >= 2:
        score += 1

    return score


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY is not set.")

    inputs = read_inputs(INPUT_FILE)

    rows = []

    for index, requirement in enumerate(inputs, start=1):
        print(f"Testing Case {index}: {requirement}")

        baseline_outputs = {}
        improved_outputs = {}
        improved_scores = []

        for stage in WORKFLOW_STAGES:
            print(f"  Running Baseline - {stage}")
            baseline_outputs[stage] = baseline_response(requirement, stage)

            print(f"  Running Improved - {stage}")
            improved_outputs[stage] = improved_response(requirement, stage)

            score = evaluate_improved_output(improved_outputs[stage])
            improved_scores.append(score)

        average_score = round(sum(improved_scores) / len(improved_scores), 2)

        row = {
            "Case": index,
            "Input": requirement,
            "Baseline - After stakeholder request": baseline_outputs["After stakeholder request"],
            "Baseline - Before PRD writing": baseline_outputs["Before PRD writing"],
            "Baseline - Before engineering discussion": baseline_outputs["Before engineering discussion"],
            "Improved - After stakeholder request": improved_outputs["After stakeholder request"],
            "Improved - Before PRD writing": improved_outputs["Before PRD writing"],
            "Improved - Before engineering discussion": improved_outputs["Before engineering discussion"],
            "Evaluation score": average_score
        }

        rows.append(row)

    fieldnames = [
        "Case",
        "Input",
        "Baseline - After stakeholder request",
        "Baseline - Before PRD writing",
        "Baseline - Before engineering discussion",
        "Improved - After stakeholder request",
        "Improved - Before PRD writing",
        "Improved - Before engineering discussion",
        "Evaluation score"
    ]

    with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nEvaluation completed. Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()