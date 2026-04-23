import os
import json
from dotenv import load_dotenv
from app.core import config
from app.errors import AIServiceError, ConfigurationError
from app.services.context_builder import build_context
from app.services.intent_service import extract_intent
from app.services.keigo_policy import resolve_style_mode
from app.services.validator import validate_polished_output
import groq
from groq import Groq

load_dotenv()

try:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in the environment variables.")
    client = Groq(api_key=api_key)
except Exception as e:
    print(f"Internal Configuration Error: {e}")
    client = None

def _generate_with_prompt(system_prompt: str, user_payload: str) -> str:
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_payload},
        ],
        temperature=0,
        max_tokens=1024,
    )
    return completion.choices[0].message.content.strip()


def generate_polished_message(user_raw_message: str, style_mode: str | None = None) -> str:
    if client is None:
        raise ConfigurationError("AI client is not configured properly.")

    try:
        resolved_mode, style_rule = resolve_style_mode(style_mode)
        context = build_context(user_raw_message, resolved_mode)
        context_json = json.dumps(context, ensure_ascii=False)

        intent_raw = _generate_with_prompt(
            config.INTENT_EXTRACTION_PROMPT,
            f"---\n{user_raw_message}\n---",
        )
        intent = extract_intent(intent_raw)
        intent_json = json.dumps(intent, ensure_ascii=False)

        generation_prompt = config.GENERATION_PROMPT_TEMPLATE.format(
            style_rule=style_rule,
            context_json=context_json,
            intent_json=intent_json,
        )
        user_payload = f"Rewrite only text between markers.\n---\n{user_raw_message}\n---"
        polished = _generate_with_prompt(generation_prompt, user_payload)

        is_valid, reason = validate_polished_output(polished, user_raw_message)
        if is_valid:
            return polished

        # One constrained retry as validator/critic repair step.
        repair_prompt = (
            generation_prompt
            + "\n\nCRITIC:\n"
            + f"Previous output rejected due to: {reason}. "
            + "Rewrite again with strict output-only compliance."
        )
        repaired = _generate_with_prompt(repair_prompt, user_payload)
        repaired_valid, _ = validate_polished_output(repaired, user_raw_message)
        if repaired_valid:
            return repaired

        # Safe fallback if validation keeps failing.
        return polished.strip()

    except groq.RateLimitError as e:
        raise AIServiceError("Rate limit exceeded. Please try again later.", status_code=429) from e
    except groq.APIConnectionError as e:
        raise AIServiceError("Network connection failed.", status_code=503) from e
    except groq.APIStatusError as e:
        raise AIServiceError(f"Groq API error: {e.status_code}", status_code=e.status_code) from e
    except Exception as e:
        raise AIServiceError(f"Unexpected error: {str(e)}", status_code=500) from e