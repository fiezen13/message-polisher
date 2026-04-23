from unittest.mock import patch


def test_generate_polished_message_returns_first_valid_output():
    with patch("app.services.ai_service._generate_with_prompt") as mocked:
        mocked.side_effect = [
            '{"intent":"ask approval","key_facts":[],"ambiguity":""}',
            "承認いただけますと幸いです。",
        ]
        from app.services.ai_service import generate_polished_message

        output = generate_polished_message("pls approve", style_mode="neutral_business")
        assert output == "承認いただけますと幸いです。"
        assert mocked.call_count == 2


def test_generate_polished_message_triggers_repair_when_invalid():
    with patch("app.services.ai_service._generate_with_prompt") as mocked:
        mocked.side_effect = [
            '{"intent":"ask approval","key_facts":[],"ambiguity":""}',
            "Output: 承認してください。",
            "承認のほど、よろしくお願いいたします。",
        ]
        from app.services.ai_service import generate_polished_message

        output = generate_polished_message("approve")
        assert output == "承認のほど、よろしくお願いいたします。"
        assert mocked.call_count == 3
