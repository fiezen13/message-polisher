from dataclasses import asdict, dataclass

from app.core import config


@dataclass
class ResolvedContext:
    source_language: str
    target_language: str
    recipient_type: str
    tone: str
    purpose: str
    detail_level: str
    recipient_guidance: str
    purpose_guidance: str
    detail_guidance: str

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_context(
    source_language: str,
    target_language: str,
    recipient_type: str,
    tone: str,
    purpose: str,
    detail_level: str,
) -> ResolvedContext:
    recipient = recipient_type if recipient_type in config.RECIPIENT_GUIDANCE else "unknown"
    intent_purpose = purpose if purpose in config.PURPOSE_GUIDANCE else "other"
    resolved_tone = tone if tone in config.TONE_TO_STYLE_MODE else "neutral"
    resolved_detail = detail_level if detail_level in config.DETAIL_GUIDANCE else "balanced"

    return ResolvedContext(
        source_language=source_language or "vi",
        target_language=target_language or "ja",
        recipient_type=recipient,
        tone=resolved_tone,
        purpose=intent_purpose,
        detail_level=resolved_detail,
        recipient_guidance=config.RECIPIENT_GUIDANCE[recipient],
        purpose_guidance=config.PURPOSE_GUIDANCE[intent_purpose],
        detail_guidance=config.DETAIL_GUIDANCE[resolved_detail],
    )
