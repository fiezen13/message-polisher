def build_prompt(message: str) -> str:
    prompt = f"""
Rewrite the following message to make it more polite and professional. 
Keep the original meaning intact, but improve the tone and clarity.

Message:
{message}
"""
    return prompt.strip()