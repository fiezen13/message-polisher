from app.services.intent_service import extract_intent


def test_extract_intent_from_json():
    raw = '{"intent":"request schedule update","key_facts":["10:00","Tokyo"],"ambiguity":""}'
    result = extract_intent(raw)
    assert result["intent"] == "request schedule update"
    assert result["key_facts"] == ["10:00", "Tokyo"]
    assert result["ambiguity"] == ""


def test_extract_intent_handles_non_json():
    result = extract_intent("not json")
    assert result["ambiguity"] == "non_json_response"
