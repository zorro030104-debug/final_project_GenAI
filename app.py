import os
import streamlit as st
from openai import OpenAI

client = OpenAI()

st.set_page_config(
    page_title="AI Requirement Clarifier",
    page_icon="🧩",
    layout="wide"
)

st.title("🧩 AI Requirement Agent")
st.subheader("Turn vague ToB requirements into structured, actionable requirement documents.")

st.markdown(
    """
    This tool helps product teams clarify vague stakeholder requests before development starts.
    It supports quick comparison modes and a multi-step requirement Agent workflow.
    """
)

with st.sidebar:
    st.header("About This Tool")
    st.markdown(
        """
        **Target users:**  
        Product managers and business analysts.

        **Workflow:**  
        1. Enter a vague requirement  
        2. Choose a project stage  
        3. Run analysis, clarification, document drafting, and review  

        **Baseline:** simple summary  
        **Improved:** structured clarification
        **Agent Workflow:** iterative PM Copilot flow
        """
    )

    st.divider()

    st.markdown(
        """
        **Improved output includes:**
        - Clarified Requirement
        - Missing Information
        - Clarification Questions
        - Risks / Ambiguities

        **Agent Workflow includes:**
        - Requirement Analysis
        - Clarification Questions
        - Stakeholder Answers
        - Requirement Document
        - Review Result
        """
    )

example_inputs = {
    "Dashboard": "Users have requested a dashboard to monitor system performance and metrics in a more structured way.",
    "Checkout UX": "Users report that the checkout process is slow and confusing, and it needs improvement.",
    "Approval Workflow": "The finance team wants better approval workflows for expense requests.",
    "Very Vague": "A stakeholder simply said: make it better."
}

st.markdown("### Try an Example")

cols = st.columns(4)

selected_example = None

for i, (label, text) in enumerate(example_inputs.items()):
    with cols[i]:
        if st.button(label):
            selected_example = text

if "requirement_input" not in st.session_state:
    st.session_state.requirement_input = ""

if selected_example:
    st.session_state.requirement_input = selected_example

st.markdown("### Requirement Input")

user_input = st.text_area(
    "Enter a vague or incomplete business requirement:",
    value=st.session_state.requirement_input,
    height=140
)

mode = st.radio(
    "Choose mode:",
    ["Baseline", "Improved", "Agent Workflow"],
    horizontal=True
)

workflow_stage = st.selectbox(
    "Workflow stage",
    [
        "After stakeholder request",
        "Before PRD writing",
        "Before engineering discussion"
    ]
)

def call_openai(prompt, temperature):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )

    return response.choices[0].message.content


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

    return call_openai(prompt, 0.5)

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

def evaluation_checklist(result):
    checklist = {
        "Contains clarified requirement": "Clarified Requirement" in result or "Clarified Requirement Draft" in result,
        "Identifies missing information": "Missing Information" in result,
        "Includes clarification questions": "Clarification Questions" in result,
        "Includes internal checks": "Internal Checks" in result,
        "Includes next actions": "Next Actions" in result,
        "Mentions risks or ambiguities": "Risks" in result or "Ambiguities" in result,
        "Separates assumptions": "Assumptions" in result
    }

    return checklist

st.markdown("---")

if mode != "Agent Workflow" and st.button("Generate"):
    if user_input.strip() == "":
        st.warning("Please enter a stakeholder requirement.")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY is not set. Please set your API key before using the app.")
    else:
        try:
            with st.spinner("Generating PM analysis..."):
                if mode == "Baseline":
                    result = baseline_response(user_input, workflow_stage)
                else:
                    result = improved_response(user_input, workflow_stage)

            st.markdown(result)

            if mode == "Improved":
                st.subheader("Evaluation Checklist")
                checklist = evaluation_checklist(result)

                for item, passed in checklist.items():
                    st.write(f"{'✅' if passed else '❌'} {item}")
                st.markdown("### Output")

            st.download_button(
                label="Download Output",
                data=result,
                file_name=f"{mode.lower()}_output.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error("An error occurred while generating the response.")
            st.code(str(e))

if mode == "Agent Workflow":
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = ""
    if "clarification_questions" not in st.session_state:
        st.session_state.clarification_questions = ""
    if "stakeholder_answers" not in st.session_state:
        st.session_state.stakeholder_answers = ""
    if "requirement_document" not in st.session_state:
        st.session_state.requirement_document = ""
    if "review_result" not in st.session_state:
        st.session_state.review_result = ""

    st.markdown("### Agent Workflow")

    if user_input.strip() == "":
        st.info("Enter a stakeholder requirement to start the Agent workflow.")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY is not set. Please set your API key before using the app.")
    else:
        step_1, step_2, step_3, step_4 = st.columns(4)

        with step_1:
            run_analysis = st.button("1. Analyze")
        with step_2:
            run_questions = st.button("2. Ask")
        with step_3:
            run_document = st.button("3. Draft")
        with step_4:
            run_review = st.button("4. Review")

        try:
            if run_analysis:
                with st.spinner("Analyzing requirement..."):
                    st.session_state.analysis_result = analyze_requirement_agent(
                        user_input,
                        workflow_stage
                    )

            if run_questions:
                if not st.session_state.analysis_result:
                    st.warning("Run Analyze before generating clarification questions.")
                else:
                    with st.spinner("Generating clarification questions..."):
                        st.session_state.clarification_questions = clarification_question_agent(
                            user_input,
                            workflow_stage,
                            st.session_state.analysis_result
                        )

            st.markdown("#### Stakeholder Answers")
            st.session_state.stakeholder_answers = st.text_area(
                "Add stakeholder answers or new information:",
                value=st.session_state.stakeholder_answers,
                height=140
            )

            if run_document:
                if not st.session_state.analysis_result:
                    st.warning("Run Analyze before drafting the requirement document.")
                elif not st.session_state.clarification_questions:
                    st.warning("Run Ask before drafting the requirement document.")
                else:
                    with st.spinner("Drafting requirement document..."):
                        st.session_state.requirement_document = requirement_document_agent(
                            user_input,
                            workflow_stage,
                            st.session_state.analysis_result,
                            st.session_state.clarification_questions,
                            st.session_state.stakeholder_answers
                        )

            if run_review:
                if not st.session_state.requirement_document:
                    st.warning("Run Draft before reviewing the requirement document.")
                else:
                    with st.spinner("Reviewing requirement document..."):
                        st.session_state.review_result = review_agent(
                            st.session_state.requirement_document
                        )

        except Exception as e:
            st.error("An error occurred while running the Agent workflow.")
            st.code(str(e))

        if st.session_state.analysis_result:
            st.markdown("### Requirement Analysis")
            st.markdown(st.session_state.analysis_result)

        if st.session_state.clarification_questions:
            st.markdown("### Clarification Questions")
            st.markdown(st.session_state.clarification_questions)

        if st.session_state.requirement_document:
            st.markdown("### Requirement Document")
            st.markdown(st.session_state.requirement_document)

        if st.session_state.review_result:
            st.markdown("### Review Result")
            st.markdown(st.session_state.review_result)

        final_output = "\n\n".join(
            [
                "# Requirement Analysis",
                st.session_state.analysis_result,
                "# Clarification Questions",
                st.session_state.clarification_questions,
                "# Stakeholder Answers",
                st.session_state.stakeholder_answers,
                "# Requirement Document",
                st.session_state.requirement_document,
                "# Review Result",
                st.session_state.review_result
            ]
        )

        st.download_button(
            label="Download Agent Output",
            data=final_output,
            file_name="agent_requirement_output.txt",
            mime="text/plain"
        )

st.markdown("---")

st.caption(
    "Note: This tool is designed to support early-stage requirement clarification. "
    "Human review is still required before finalizing any business requirement."
)
