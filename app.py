import os
import streamlit as st
from openai import OpenAI

client = OpenAI()

st.title("AI Requirement Clarifier")

st.write("Enter a vague business requirement and get a structured clarification.")

st.caption("Baseline: simple summary. Improved: structured requirement clarification.")

user_input = st.text_area("Enter requirement:")

mode = st.selectbox("Choose mode", ["Baseline", "Improved"])


def baseline_response(text):
    prompt = f"""
Summarize the following business requirement in 2-3 sentences.

Requirement:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


def improved_response(text):
    prompt = f"""
You are a professional product manager helping clarify vague ToB business requirements.

Given a vague requirement, produce structured output in the following format:

### Clarified Requirement
Rewrite the requirement clearly without inventing details.

### Missing Information
List key missing details, such as users, goals, data, constraints, scope, success metrics, and timeline.

### Clarification Questions
List useful follow-up questions a product manager should ask.

### Risks / Ambiguities
Identify risks, unclear assumptions, possible scope creep, and areas requiring human review.

Requirement:
{text}

Important:
- Do NOT invent facts.
- If information is unclear or missing, explicitly say so.
- Be concise but useful.
- Focus on practical ToB product workflow clarification.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


if st.button("Generate"):
    if user_input.strip() == "":
        st.warning("Please enter a requirement.")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY is not set. Please set your API key before using the app.")
    else:
        try:
            with st.spinner("Generating response..."):
                if mode == "Baseline":
                    result = baseline_response(user_input)
                else:
                    result = improved_response(user_input)

            st.markdown(result)

        except Exception as e:
            st.error("An error occurred while generating the response.")
            st.code(str(e))