def _detect_situation(text: str) -> str:
    """Infer a coarse situation label from Japanese keywords."""
    leave_keywords = ("休", "有給", "休暇", "欠勤")
    schedule_keywords = ("日程", "スケジュール", "変更", "延期", "リスケ")
    apology_keywords = ("すみません", "申し訳", "失礼")
    request_keywords = ("お願い", "ください", "ご確認", "いただけます")

    if any(keyword in text for keyword in leave_keywords):
        return "request_leave"
    if any(keyword in text for keyword in schedule_keywords):
        return "schedule_change"
    if any(keyword in text for keyword in apology_keywords):
        return "apology"
    if any(keyword in text for keyword in request_keywords):
        return "request"
    return "general"


def build_context(raw_text: str, style_mode: str) -> dict:
    """Build semantic + technical context for Japanese rewriting."""
    has_multiline = "\n" in raw_text
    situation = _detect_situation(raw_text)

    # Conservative defaults: avoid inventing relationships unless signal is present.
    speaker_role = "unknown"
    listener_role = "unknown"

    if any(keyword in raw_text for keyword in ("部長", "課長", "マネージャ", "上司")):
        speaker_role = "employee"
        listener_role = "manager"
    elif any(keyword in raw_text for keyword in ("お客様", "顧客", "クライアント")):
        speaker_role = "staff"
        listener_role = "customer"

    return {
        "speaker_role": speaker_role,
        "listener_role": listener_role,
        "situation": situation,
        "formality": style_mode,
        "has_multiline": has_multiline,
        "channel": "chat",
    }
