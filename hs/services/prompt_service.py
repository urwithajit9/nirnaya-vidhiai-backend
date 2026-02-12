def build_predict_prompt(user_description, candidates):

    candidate_text = "\n".join(
        [f"{c['hs_code']} - {c['description']}" for c in candidates]
    )

    return f"""
You are an expert Indian Customs HS classification assistant.

Product Description:
{user_description}

Candidate HS Codes (choose ONLY from below):
{candidate_text}

Instructions:
1. Select the MOST appropriate HS code from the provided list.
2. Do NOT invent a new code.
3. Justify selection referencing description language.
4. Output format:

HS Code: <code>
Reasoning: <short explanation>
"""


def build_analysis_prompt():
    return """
You are a trade compliance assistant.

Use ONLY provided context.
Do NOT assume missing data.
If information not found, say:
"Not available in database."

Provide:

1. Policy Interpretation
2. Compliance Risk
3. Importer Checklist
4. Practical Notes
"""


def build_qa_prompt(question: str):
    return f"""
You are a regulatory assistant.

Answer ONLY using provided context.
If not found, say:
"The requested information is not available in the database."

QUESTION:
{question}
"""
