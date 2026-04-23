import json


def extract_intent(raw_response: str) -> dict:
    """Parse and normalize JSON response for intent extraction."""
    try:
        parsed = json.loads(raw_response)
    except json.JSONDecodeError:
        return {"intent": "", "key_facts": [], "ambiguity": "non_json_response"}

    intent = str(parsed.get("intent", "")).strip()
    ambiguity = str(parsed.get("ambiguity", "")).strip()

    key_facts = parsed.get("key_facts", [])
    if not isinstance(key_facts, list):
        key_facts = []
    key_facts = [str(item).strip() for item in key_facts if str(item).strip()]

    return {"intent": intent, "key_facts": key_facts, "ambiguity": ambiguity}
