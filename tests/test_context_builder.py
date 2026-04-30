from app.services.context_builder import build_context


def test_build_context_defaults_to_unknown_roles():
    context = build_context("確認お願いします", "neutral_business")
    assert context.speaker_role == "unknown"
    assert context.listener_role == "unknown"
    assert context.formality == "neutral_business"
    assert context.situation == "request"
    assert context.to_dict()["channel"] == "chat"


def test_build_context_detects_leave_request():
    context = build_context("明日は有給で休みを取りたいです。", "formal_keigo")
    assert context.situation == "request_leave"
    assert context.formality == "formal_keigo"


def test_build_context_detects_manager_relation():
    context = build_context("部長、日程変更のご相談です。", "neutral_business")
    assert context.speaker_role == "employee"
    assert context.listener_role == "manager"
    assert context.situation == "schedule_change"
