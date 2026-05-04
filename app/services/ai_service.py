import os
import json
from dotenv import load_dotenv
from app.core import config
from app.errors import AIServiceError, ConfigurationError
from app.services.context_builder import build_context
from app.services.context_resolver import resolve_context
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

def _generate_with_prompt(system_prompt: str, user_payload: str, temperature: float = 0.0) -> str:
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_payload},
        ],
        temperature=temperature,
        max_tokens=1024,
    )
    return completion.choices[0].message.content.strip()


def _build_generation_prompt(
    style_rule: str,
    context_json: str,
    intent_json: str,
    source_language: str = "ja",
    target_language: str = "ja",
    recipient_guidance: str | None = None,
    purpose_guidance: str | None = None,
    detail_guidance: str | None = None,
) -> str:
    prompt = config.GENERATION_PROMPT_TEMPLATE.format(
        style_rule=style_rule,
        context_json=context_json,
        intent_json=intent_json,
    )
    if recipient_guidance:
        prompt += f"\n\nRECIPIENT GUIDANCE:\n{recipient_guidance}"
    if purpose_guidance:
        prompt += f"\n\nPURPOSE GUIDANCE:\n{purpose_guidance}"
    if detail_guidance:
        prompt += f"\n\nDETAIL LEVEL GUIDANCE:\n{detail_guidance}"
    prompt += (
        "\n\nLANGUAGE CONSTRAINT:\n"
        f"- Source language: {source_language}\n"
        f"- Output language must be: {target_language}\n"
        "- Preserve intent and key facts from INTENT JSON; do not invent facts.\n"
        "- If the source is not Japanese, translate meaning into natural Japanese, not word-by-word."
    )
    return prompt


def _build_intent_prompt(source_language: str) -> str:
    return (
        "You are extracting communication intent from user text for rewriting.\n"
        f"The source text language is: {source_language}.\n"
        "Return ONLY valid JSON with keys:\n"
        "- intent: short summary of what user wants to communicate\n"
        "- key_facts: list of important facts to preserve (names, numbers, dates, times, urls)\n"
        "- ambiguity: brief note if meaning is unclear, else empty string\n"
        "Do not add markdown, comments, or any extra text."
    )


def _run_rewrite_pipeline(
    user_raw_message: str,
    style_mode: str | None = None,
    source_language: str = "ja",
    target_language: str = "ja",
    recipient_guidance: str | None = None,
    purpose_guidance: str | None = None,
    detail_guidance: str | None = None,
) -> tuple[str, dict]:
    resolved_mode, style_rule = resolve_style_mode(style_mode)
    context = build_context(user_raw_message, resolved_mode)
    context_json = json.dumps(context.to_dict(), ensure_ascii=False)

    intent_raw = _generate_with_prompt(
        _build_intent_prompt(source_language),
        f"---\n{user_raw_message}\n---",
        temperature=0.0,
    )
    intent = extract_intent(intent_raw)
    intent_json = json.dumps(intent, ensure_ascii=False)

    generation_prompt = _build_generation_prompt(
        style_rule=style_rule,
        context_json=context_json,
        intent_json=intent_json,
        source_language=source_language,
        target_language=target_language,
        recipient_guidance=recipient_guidance,
        purpose_guidance=purpose_guidance,
        detail_guidance=detail_guidance,
    )
    rewrite_temperature = 0.35 if source_language != "ja" else 0.2
    user_payload = (
        "Rewrite only text between markers into natural business Japanese.\n"
        "Do not output anything outside the markers.\n"
        f"---\n{user_raw_message}\n---"
    )
    polished = _generate_with_prompt(generation_prompt, user_payload, temperature=rewrite_temperature)

    is_valid, reason = validate_polished_output(
        polished,
        user_raw_message,
        key_facts=intent.get("key_facts", []),
    )
    if is_valid:
        return polished, intent

    repair_prompt = (
        generation_prompt
        + "\n\nCRITIC:\n"
        + f"Previous output rejected due to: {reason}. "
        + "Rewrite again with strict output-only compliance."
    )
    repaired = _generate_with_prompt(repair_prompt, user_payload, temperature=rewrite_temperature)
    repaired_valid, _ = validate_polished_output(
        repaired,
        user_raw_message,
        key_facts=intent.get("key_facts", []),
    )
    if repaired_valid:
        return repaired, intent

    return polished.strip(), intent


def _generate_variant(base_message: str, variant_name: str, variant_rule: str) -> str:
    prompt = (
        "You rewrite Japanese text according to style instruction.\n"
        "Return only rewritten Japanese sentence.\n\n"
        f"STYLE: {variant_name}\n"
        f"RULE: {variant_rule}"
    )
    user_payload = f"Rewrite text between markers.\n---\n{base_message}\n---"
    variant = _generate_with_prompt(prompt, user_payload, temperature=0.25)
    return variant.strip() or base_message


def generate_polished_message(user_raw_message: str, style_mode: str | None = None) -> str:
    if client is None:
        raise ConfigurationError("AI client is not configured properly.")

    try:
        polished, _ = _run_rewrite_pipeline(
            user_raw_message,
            style_mode=style_mode,
            source_language="ja",
            target_language="ja",
        )
        return polished
    except groq.RateLimitError as e:
        raise AIServiceError("Rate limit exceeded. Please try again later.", status_code=429) from e
    except groq.APIConnectionError as e:
        raise AIServiceError("Network connection failed.", status_code=503) from e
    except groq.APIStatusError as e:
        raise AIServiceError(f"Groq API error: {e.status_code}", status_code=e.status_code) from e
    except Exception as e:
        raise AIServiceError(f"Unexpected error: {str(e)}", status_code=500) from e


def generate_polish_result(
    original_message: str,
    recipient_type: str,
    tone: str,
    purpose: str,
    language: str = "ja",
    source_language: str = "vi",
    detail_level: str = "balanced",
) -> dict:
    if client is None:
        raise ConfigurationError("AI client is not configured properly.")

    try:
        resolved = resolve_context(
            source_language=source_language,
            target_language=language,
            recipient_type=recipient_type,
            tone=tone,
            purpose=purpose,
            detail_level=detail_level,
        )
        style_mode = config.TONE_TO_STYLE_MODE[resolved.tone]
        rewritten_message, intent = _run_rewrite_pipeline(
            original_message,
            style_mode=style_mode,
            source_language=resolved.source_language,
            target_language=resolved.target_language,
            recipient_guidance=resolved.recipient_guidance,
            purpose_guidance=resolved.purpose_guidance,
            detail_guidance=resolved.detail_guidance,
        )

        quick_variants = {
            "formal": _generate_variant(
                rewritten_message,
                "formal",
                config.VARIANT_STYLE_RULES["formal"],
            ),
            "friendly": _generate_variant(
                rewritten_message,
                "friendly",
                config.VARIANT_STYLE_RULES["friendly"],
            ),
            "concise": _generate_variant(
                rewritten_message,
                "concise",
                config.VARIANT_STYLE_RULES["concise"],
            ),
            "highly_professional": _generate_variant(
                rewritten_message,
                "highly_professional",
                config.VARIANT_STYLE_RULES["highly_professional"],
            ),
        }

        ambiguity = intent.get("ambiguity", "")
        return {
            "rewritten_message": rewritten_message,
            "quick_variants": quick_variants,
            "meta": {
                "intent": intent.get("intent", ""),
                "ambiguity": ambiguity,
                "confidence": 0.6 if ambiguity else 0.85,
                "warnings": [ambiguity] if ambiguity else [],
            },
            "safety_flags": {
                "ambiguous_input": bool(ambiguity),
                "missing_context": resolved.recipient_type == "unknown" or resolved.purpose == "other",
                "potentially_risky": False,
            },
        }
    except groq.RateLimitError as e:
        raise AIServiceError("Rate limit exceeded. Please try again later.", status_code=429) from e
    except groq.APIConnectionError as e:
        raise AIServiceError("Network connection failed.", status_code=503) from e
    except groq.APIStatusError as e:
        raise AIServiceError(f"Groq API error: {e.status_code}", status_code=e.status_code) from e
    except Exception as e:
        raise AIServiceError(f"Unexpected error: {str(e)}", status_code=500) from e