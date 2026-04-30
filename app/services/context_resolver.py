from dataclasses import asdict, dataclass

from app.core import config


@dataclass
class ResolvedContext:
    language: str
    recipient_type: str
    tone: str
    purpose: str
    recipient_guidance: str
    purpose_guidance: str

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_context(language: str, recipient_type: str, tone: str, purpose: str) -> ResolvedContext:
    recipient = recipient_type if recipient_type in config.RECIPIENT_GUIDANCE else "unknown"
    intent_purpose = purpose if purpose in config.PURPOSE_GUIDANCE else "other"
    resolved_tone = tone if tone in config.TONE_TO_STYLE_MODE else "neutral"

    return ResolvedContext(
        language=language or "ja",
        recipient_type=recipient,
        tone=resolved_tone,
        purpose=intent_purpose,
        recipient_guidance=config.RECIPIENT_GUIDANCE[recipient],
        purpose_guidance=config.PURPOSE_GUIDANCE[intent_purpose],
    )
