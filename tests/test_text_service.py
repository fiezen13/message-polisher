from app.services.text_service import clean_text


def test_clean_text():
    cases = [
        ("", ""),
        ("   ", ""),
        ("  hello  world  ", "hello world"),
        ("a  b\nc", "a b\nc"),
        ("line1\n\nline2", "line1\nline2"),
    ]
    for raw, expected in cases:
        assert clean_text(raw) == expected
