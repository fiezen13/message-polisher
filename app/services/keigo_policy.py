from app.core import config


def resolve_style_mode(style_mode: str | None) -> tuple[str, str]:
    """Resolve style mode and return (mode, style_rule)."""
    if style_mode and style_mode in config.STYLE_RULES:
        return style_mode, config.STYLE_RULES[style_mode]
    return config.DEFAULT_STYLE_MODE, config.STYLE_RULES[config.DEFAULT_STYLE_MODE]
