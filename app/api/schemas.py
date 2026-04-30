from typing import Literal

from pydantic import BaseModel, Field


RecipientType = Literal["professor", "recruiter", "manager", "client", "teammate", "unknown"]
ToneType = Literal["formal", "apologetic", "friendly", "assertive", "neutral"]
PurposeType = Literal[
    "request_extension",
    "follow_up",
    "apology",
    "scheduling",
    "escalation",
    "gratitude",
    "other",
]


class PolishConstraints(BaseModel):
    max_length: int | None = Field(default=None, ge=20, le=3000)
    keep_keywords: list[str] = Field(default_factory=list)


class PolishRequest(BaseModel):
    language: Literal["ja"] = "ja"
    original_message: str = Field(min_length=1, max_length=3000)
    recipient_type: RecipientType = "unknown"
    tone: ToneType = "neutral"
    purpose: PurposeType = "other"
    constraints: PolishConstraints | None = None


class QuickVariants(BaseModel):
    formal: str
    friendly: str
    concise: str
    highly_professional: str


class PolishMeta(BaseModel):
    intent: str
    ambiguity: str
    confidence: float
    warnings: list[str]


class SafetyFlags(BaseModel):
    ambiguous_input: bool
    missing_context: bool
    potentially_risky: bool


class PolishResponse(BaseModel):
    rewritten_message: str
    explanations: list[str]
    quick_variants: QuickVariants
    meta: PolishMeta
    safety_flags: SafetyFlags
