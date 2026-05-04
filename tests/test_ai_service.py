from unittest.mock import patch


def test_generate_polished_message_returns_first_valid_output():
    with patch("app.services.ai_service._generate_with_prompt") as mocked:
        mocked.side_effect = [
            '{"intent":"ask approval","key_facts":["10:00"],"ambiguity":""}',
            "10:00までに承認いただけますと幸いです。",
        ]
        from app.services.ai_service import generate_polished_message

        output = generate_polished_message("pls approve", style_mode="neutral_business")
        assert output == "10:00までに承認いただけますと幸いです。"
        assert mocked.call_count == 2


def test_generate_polished_message_triggers_repair_when_invalid():
    with patch("app.services.ai_service._generate_with_prompt") as mocked:
        mocked.side_effect = [
            '{"intent":"ask approval","key_facts":["10:00"],"ambiguity":""}',
            "承認してください。",
            "10:00までに承認のほど、よろしくお願いいたします。",
        ]
        from app.services.ai_service import generate_polished_message

        output = generate_polished_message("approve")
        assert output == "10:00までに承認のほど、よろしくお願いいたします。"
        assert mocked.call_count == 3


def test_generate_polish_result_supports_vi_to_ja_pipeline():
    with patch("app.services.ai_service.resolve_context") as mock_resolve, patch(
        "app.services.ai_service._run_rewrite_pipeline"
    ) as mock_pipeline, patch("app.services.ai_service._generate_variant") as mock_variant:
        from app.services.ai_service import generate_polish_result
        from app.services.context_resolver import ResolvedContext

        mock_resolve.return_value = ResolvedContext(
            source_language="vi",
            target_language="ja",
            recipient_type="professor",
            tone="formal",
            purpose="request_extension",
            detail_level="balanced",
            recipient_guidance="Use respectful language suitable for academic communication.",
            purpose_guidance="State the request clearly and include a brief, respectful reason.",
            detail_guidance="balanced guidance",
        )
        mock_pipeline.return_value = (
            "恐れ入りますが、締切を2日延長いただけますでしょうか。",
            {"intent": "request_extension", "ambiguity": "", "key_facts": ["2日"]},
        )
        mock_variant.side_effect = [
            "formal-v",
            "friendly-v",
            "concise-v",
            "professional-v",
        ]

        result = generate_polish_result(
            original_message="Em muốn xin lùi deadline thêm 2 ngày",
            recipient_type="professor",
            tone="formal",
            purpose="request_extension",
            language="ja",
            source_language="vi",
        )

        assert result["rewritten_message"]
        assert result["quick_variants"]["formal"] == "formal-v"
        mock_resolve.assert_called_once()
        _, kwargs = mock_resolve.call_args
        assert kwargs["source_language"] == "vi"
        assert kwargs["target_language"] == "ja"
        assert kwargs["detail_level"] == "balanced"
