DEFAULT_STYLE_MODE = "neutral_business"

STYLE_RULES = {
    "neutral_business": (
        "Use polite Japanese (desu/masu). Neutral, professional, and concise. "
        "Do not overuse honorific expressions."
    ),
    "formal_keigo": (
        "Use formal business keigo suitable for customers or external partners. "
        "Prefer respectful and humble forms where appropriate."
    ),
    "casual_polite": (
        "Use friendly but polite Japanese. Keep desu/masu, avoid very stiff keigo."
    ),
}

RECIPIENT_GUIDANCE = {
    "professor": "Use respectful language suitable for academic communication.",
    "recruiter": "Use concise and professional language suitable for hiring communication.",
    "manager": "Use polite internal-business wording with clear accountability.",
    "client": "Use formal customer-facing wording with careful tone.",
    "teammate": "Use polite and collaborative wording.",
    "unknown": "Use neutral polite wording without assuming hierarchy.",
}

PURPOSE_GUIDANCE = {
    "request_extension": "State the request clearly and include a brief, respectful reason.",
    "follow_up": "Be concise, reference prior context, and ask for next-step confirmation.",
    "apology": "Acknowledge inconvenience and use sincere, non-defensive wording.",
    "scheduling": "Clarify proposed time/date and ask for confirmation politely.",
    "escalation": "Describe issue factually and request support calmly.",
    "gratitude": "Express thanks clearly and professionally.",
    "other": "Keep the message natural and context-appropriate.",
}

TONE_TO_STYLE_MODE = {
    "formal": "formal_keigo",
    "apologetic": "formal_keigo",
    "friendly": "casual_polite",
    "assertive": "neutral_business",
    "neutral": "neutral_business",
}

VARIANT_STYLE_RULES = {
    "formal": "Use formal business keigo, concise and respectful.",
    "friendly": "Use warm but polite language. Keep it natural and approachable.",
    "concise": "Keep the sentence brief while preserving all key facts.",
    "highly_professional": "Use highly polished professional Japanese suitable for external stakeholders.",
}

INTENT_EXTRACTION_PROMPT = (
    "You are extracting intent from Japanese user text for rewriting.\n"
    "Return ONLY valid JSON with keys:\n"
    "- intent: short summary of what user wants to communicate\n"
    "- key_facts: list of important facts to preserve (names, numbers, dates, times, urls)\n"
    "- ambiguity: brief note if meaning is unclear, else empty string\n"
    "Do not add markdown, comments, or any extra text."
)

GENERATION_PROMPT_TEMPLATE = (
    "You are a Japanese message polishing assistant.\n\n"
    "TASK:\n"
    "Rewrite user input into natural, polite, professional Japanese.\n\n"
    "STYLE POLICY:\n"
    "{style_rule}\n\n"
    "CONSTRAINTS:\n"
    "- Preserve original meaning exactly. Do not invent new facts.\n"
    "- Keep names, numbers, dates, times, and URLs unchanged.\n"
    "- Do not invent speaker/listener relationship.\n"
    "- If context is unclear, prefer neutral polite wording.\n"
    "- Return ONLY rewritten Japanese text.\n\n"
    "CONTEXT JSON:\n"
    "{context_json}\n\n"
    "INTENT JSON:\n"
    "{intent_json}"
)

EXPLANATION_PROMPT_TEMPLATE = (
    "You are a writing coach.\n"
    "Given original and rewritten Japanese messages, return ONLY valid JSON with key `explanations`.\n"
    "`explanations` must be a list of 2 to 4 short English bullets describing meaningful changes.\n"
    "No markdown, no extra keys.\n\n"
    "CONTEXT:\n"
    "{context_json}\n\n"
    "ORIGINAL:\n"
    "{original}\n\n"
    "REWRITTEN:\n"
    "{rewritten}"
)
