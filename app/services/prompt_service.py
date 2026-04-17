def build_prompt(message: str) -> str:
    prompt = f"""
"Rewrite this Vietnamese message to be more polite and professional. ONLY return the polished text, no explanation, no translation." 
Keep the original meaning intact, but improve the tone and clarity.

Message:
{message}
"""
    return prompt.strip()