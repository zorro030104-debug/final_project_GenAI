import os
import streamlit as st
from openai import OpenAI

client = OpenAI()

st.set_page_config(
    page_title="AI Requirement Clarifier",
    page_icon="🧩",
    layout="wide"
)

st.title("🧩 AI Requirement Clarifier")
st.subheader("Turn vague ToB requirements into structured, actionable specifications.")

st.markdown(
    """
    This tool helps product teams clarify vague stakeholder requests before development starts.
    It compares a simple baseline summary with a structured GenAI clarification workflow.
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
        2. Choose Baseline or Improved mode  
        3. Review the generated output  

        **Baseline:** simple summary  
        **Improved:** structured clarification
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
    ["Baseline", "Improved"],
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
        messages=[
            {"role": "user", "content": prompt}
        ],
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
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

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

if st.button("Generate"):
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

st.markdown("---")

st.caption(
    "Note: This tool is designed to support early-stage requirement clarification. "
    "Human review is still required before finalizing any business requirement."
)