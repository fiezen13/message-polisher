from app.core import config
from app.services.keigo_policy import resolve_style_mode


def test_resolve_style_mode_valid():
    mode, rule = resolve_style_mode("formal_keigo")
    assert mode == "formal_keigo"
    assert "keigo" in rule.lower()


def test_resolve_style_mode_fallback():
    mode, rule = resolve_style_mode("unknown_mode")
    assert mode == config.DEFAULT_STYLE_MODE
    assert rule == config.STYLE_RULES[config.DEFAULT_STYLE_MODE]
