import os
from openai import OpenAI

client = OpenAI()

def baseline_response(text):
    """
    Baseline: simple prompt-only summarization
    """
    prompt = f"Summarize the following requirement:\n{text}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


def improved_response(text):
    """
    Improved: structured requirement clarification
    """
    prompt = f"""
You are a professional product manager helping clarify vague business requirements.

Given a vague requirement, produce structured output in the following format:

### Clarified Requirement
Rewrite the requirement clearly.

### Missing Information
List key missing details.

### Clarification Questions
List useful follow-up questions.

### Risks / Ambiguities
Identify risks or unclear areas.

Requirement:
{text}

Important:
- Do NOT invent facts
- If unclear, say so
- Be concise but useful
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


def main():
    print("=== AI Requirement Clarifier (CLI Tool) ===\n")

    user_input = input("Enter a requirement:\n> ")

    mode = input("Choose mode (baseline / improved): ").strip().lower()

    if not user_input:
        print("❌ Please enter a requirement.")
        return

    if mode == "baseline":
        result = baseline_response(user_input)
    else:
        result = improved_response(user_input)

    print("\n=== Result ===\n")
    print(result)


if __name__ == "__main__":
    main()