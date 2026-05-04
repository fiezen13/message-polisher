from app.services.context_resolver import resolve_context


def test_resolve_context_uses_supported_values():
    context = resolve_context(
        "vi", "ja", "professor", "apologetic", "request_extension", "detailed"
    )
    assert context.source_language == "vi"
    assert context.target_language == "ja"
    assert context.recipient_type == "professor"
    assert context.tone == "apologetic"
    assert context.purpose == "request_extension"
    assert context.detail_level == "detailed"
    assert "academic" in context.recipient_guidance
    assert len(context.detail_guidance) > 0


def test_resolve_context_fallbacks_for_unknown_values():
    context = resolve_context("vi", "ja", "random", "random", "random", "not_a_real_level")
    assert context.recipient_type == "unknown"
    assert context.tone == "neutral"
    assert context.purpose == "other"
    assert context.detail_level == "balanced"
