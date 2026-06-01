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


def call_openai(prompt, temperature):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
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

    return call_openai(prompt, 0.3)


def analyze_requirement_agent(text, stage):
    prompt = f"""
You are the Requirement Analysis Agent in a ToB product team.

Your task is to analyze the stakeholder input before any requirement document is written.
Do not write the final requirement document in this step.
Do not invent facts.

Return the result using exactly these sections:

### 1. Surface Requirement
Restate the stakeholder input without adding new facts.

### 2. Confirmed Information
List only information explicitly present in the stakeholder input.

### 3. Assumptions
List assumptions separately and label them as assumptions.

### 4. Ambiguities
List unclear points that block requirement definition.

### 5. Requirement Decomposition
Break the input into separate requirement parts when more than one intent exists.

### 6. Stage-Specific Focus
Explain what matters most at the selected workflow stage.

Requirement:
{text}

Workflow stage:
{stage}

Rules:
- Do not ask clarification questions in this step.
- Do not draft acceptance criteria in this step.
- Focus on PM-level requirement analysis.
"""

    return call_openai(prompt, 0.2)


def clarification_question_agent(text, stage, analysis):
    prompt = f"""
You are the Clarification Question Agent in a ToB product team.

Your task is only to generate clarification questions for the stakeholder and internal team.
Do not write the final requirement document.
Do not invent stakeholder answers.

Use the original requirement, workflow stage, and analysis result.

Return the result using exactly these sections:

### 1. Stakeholder Questions
Ask questions that clarify business goal, users, scenarios, scope, priority, and success criteria.

### 2. Internal Team Questions
Ask questions for engineering, data, operations, support, or other internal teams.

### 3. Questions Required Before PRD
List questions that must be answered before a PRD can be written.

Requirement:
{text}

Workflow stage:
{stage}

Analysis result:
{analysis}

Rules:
- Every question must reduce ambiguity.
- Do not provide answers.
- Do not suggest implementation before the requirement is clarified.
"""

    return call_openai(prompt, 0.2)


def requirement_document_agent(text, stage, analysis, questions, answers):
    prompt = f"""
You are the Requirement Document Agent in a ToB product team.

Your task is to draft a requirement document based on the available information.
Separate confirmed information, assumptions, and open questions.
Do not turn unanswered questions into facts.

Return the result using exactly these sections:

### 1. Background
Summarize the context using confirmed information.

### 2. Problem Statement
Describe the problem without adding unsupported facts.

### 3. User Need
Describe the user need based on available information.

### 4. Clarified Requirement
Write a clearer requirement draft.

### 5. Scope
List what is included.

### 6. Out of Scope
List what is not included or not yet confirmed.

### 7. Acceptance Criteria
List verifiable criteria. If information is missing, mark it as requiring confirmation.

### 8. Open Questions
List unresolved questions.

### 9. Next Actions
List practical next steps before development.

Requirement:
{text}

Workflow stage:
{stage}

Analysis result:
{analysis}

Clarification questions:
{questions}

Stakeholder answers:
{answers}

Rules:
- Do not invent metrics, business rules, user roles, or technical solutions.
- Mark assumptions clearly.
- Keep the document practical for PM review.
"""

    return call_openai(prompt, 0.2)


def review_agent(requirement_document):
    prompt = f"""
You are the Requirement Review Agent in a ToB product team.

Your task is to review the requirement document before it is used for PRD writing or engineering discussion.

Return the result using exactly these sections:

### 1. Unsupported Facts
Identify statements that appear unsupported by the provided information.

### 2. Remaining Ambiguities
List unclear points that still require confirmation.

### 3. Missing Acceptance Criteria
List acceptance criteria that are missing or not verifiable.

### 4. Readiness Assessment
State whether the document is ready for the selected workflow stage, and explain why.

### 5. Revision Suggestions
Suggest concrete revisions.

Requirement document:
{requirement_document}

Rules:
- Review the document critically.
- Do not add new requirement content.
- Focus on requirement quality, clarity, and actionability.
"""

    return call_openai(prompt, 0.1)


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


def evaluate_agent_workflow(analysis, questions, document, review):
    """
    Evaluates Agent Workflow output using a 10-point checklist.
    """
    score = 0

    surface = extract_section(analysis, "Surface Requirement")
    confirmed = extract_section(analysis, "Confirmed Information")
    assumptions = extract_section(analysis, "Assumptions")
    ambiguities = extract_section(analysis, "Ambiguities")
    decomposition = extract_section(analysis, "Requirement Decomposition")
    stakeholder_questions = extract_section(questions, "Stakeholder Questions")
    internal_questions = extract_section(questions, "Internal Team Questions")
    clarified = extract_section(document, "Clarified Requirement")
    acceptance = extract_section(document, "Acceptance Criteria")
    review_readiness = extract_section(review, "Readiness Assessment")

    if surface.strip():
        score += 1

    if confirmed.strip():
        score += 1

    if assumptions.strip():
        score += 1

    if ambiguities.strip():
        score += 1

    if decomposition.strip():
        score += 1

    if count_bullets(stakeholder_questions) >= 3:
        score += 1

    if count_bullets(internal_questions) >= 2:
        score += 1

    if clarified.strip():
        score += 1

    if count_bullets(acceptance) >= 2:
        score += 1

    if review_readiness.strip():
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
        agent_analysis_outputs = {}
        agent_question_outputs = {}
        agent_document_outputs = {}
        agent_review_outputs = {}
        improved_scores = []
        agent_scores = []

        for stage in WORKFLOW_STAGES:
            print(f"  Running Baseline - {stage}")
            baseline_outputs[stage] = baseline_response(requirement, stage)

            print(f"  Running Improved - {stage}")
            improved_outputs[stage] = improved_response(requirement, stage)

            improved_score = evaluate_improved_output(improved_outputs[stage])
            improved_scores.append(improved_score)

            print(f"  Running Agent Analysis - {stage}")
            agent_analysis_outputs[stage] = analyze_requirement_agent(requirement, stage)

            print(f"  Running Agent Questions - {stage}")
            agent_question_outputs[stage] = clarification_question_agent(
                requirement,
                stage,
                agent_analysis_outputs[stage]
            )

            print(f"  Running Agent Document - {stage}")
            agent_document_outputs[stage] = requirement_document_agent(
                requirement,
                stage,
                agent_analysis_outputs[stage],
                agent_question_outputs[stage],
                "No stakeholder answers were provided during automated evaluation."
            )

            print(f"  Running Agent Review - {stage}")
            agent_review_outputs[stage] = review_agent(agent_document_outputs[stage])

            agent_score = evaluate_agent_workflow(
                agent_analysis_outputs[stage],
                agent_question_outputs[stage],
                agent_document_outputs[stage],
                agent_review_outputs[stage]
            )
            agent_scores.append(agent_score)

        average_score = round(sum(improved_scores) / len(improved_scores), 2)
        average_agent_score = round(sum(agent_scores) / len(agent_scores), 2)

        row = {
            "Case": index,
            "Input": requirement,
            "Baseline - After stakeholder request": baseline_outputs["After stakeholder request"],
            "Baseline - Before PRD writing": baseline_outputs["Before PRD writing"],
            "Baseline - Before engineering discussion": baseline_outputs["Before engineering discussion"],
            "Improved - After stakeholder request": improved_outputs["After stakeholder request"],
            "Improved - Before PRD writing": improved_outputs["Before PRD writing"],
            "Improved - Before engineering discussion": improved_outputs["Before engineering discussion"],
            "Improved evaluation score": average_score,
            "Agent Analysis - After stakeholder request": agent_analysis_outputs["After stakeholder request"],
            "Agent Analysis - Before PRD writing": agent_analysis_outputs["Before PRD writing"],
            "Agent Analysis - Before engineering discussion": agent_analysis_outputs["Before engineering discussion"],
            "Agent Questions - After stakeholder request": agent_question_outputs["After stakeholder request"],
            "Agent Questions - Before PRD writing": agent_question_outputs["Before PRD writing"],
            "Agent Questions - Before engineering discussion": agent_question_outputs["Before engineering discussion"],
            "Agent Document - After stakeholder request": agent_document_outputs["After stakeholder request"],
            "Agent Document - Before PRD writing": agent_document_outputs["Before PRD writing"],
            "Agent Document - Before engineering discussion": agent_document_outputs["Before engineering discussion"],
            "Agent Review - After stakeholder request": agent_review_outputs["After stakeholder request"],
            "Agent Review - Before PRD writing": agent_review_outputs["Before PRD writing"],
            "Agent Review - Before engineering discussion": agent_review_outputs["Before engineering discussion"],
            "Agent evaluation score": average_agent_score
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
        "Improved evaluation score",
        "Agent Analysis - After stakeholder request",
        "Agent Analysis - Before PRD writing",
        "Agent Analysis - Before engineering discussion",
        "Agent Questions - After stakeholder request",
        "Agent Questions - Before PRD writing",
        "Agent Questions - Before engineering discussion",
        "Agent Document - After stakeholder request",
        "Agent Document - Before PRD writing",
        "Agent Document - Before engineering discussion",
        "Agent Review - After stakeholder request",
        "Agent Review - Before PRD writing",
        "Agent Review - Before engineering discussion",
        "Agent evaluation score"
    ]

    with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nEvaluation completed. Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
