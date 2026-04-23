from app.services.validator import validate_polished_output


def test_validator_rejects_empty():
    ok, reason = validate_polished_output("   ", "hello")
    assert not ok
    assert reason == "empty_output"


def test_validator_accepts_simple_text():
    ok, reason = validate_polished_output("ご確認をお願いいたします。", "confirm this")
    assert ok
    assert reason == ""
