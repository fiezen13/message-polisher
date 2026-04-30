from app.services.context_resolver import resolve_context


def test_resolve_context_uses_supported_values():
    context = resolve_context("ja", "professor", "apologetic", "request_extension")
    assert context.language == "ja"
    assert context.recipient_type == "professor"
    assert context.tone == "apologetic"
    assert context.purpose == "request_extension"
    assert "academic" in context.recipient_guidance


def test_resolve_context_fallbacks_for_unknown_values():
    context = resolve_context("ja", "random", "random", "random")
    assert context.recipient_type == "unknown"
    assert context.tone == "neutral"
    assert context.purpose == "other"
