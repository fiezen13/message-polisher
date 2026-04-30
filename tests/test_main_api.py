from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app


client = TestClient(app)


def test_polish_endpoint_returns_structured_response():
    mocked_response = {
        "rewritten_message": "恐れ入りますが、締切を2日延長いただけますでしょうか。",
        "explanations": ["Adjusted formality", "Added respectful request phrasing"],
        "quick_variants": {
            "formal": "恐れ入りますが、締切を2日延長いただけますでしょうか。",
            "friendly": "すみません、締切を2日延ばしていただけると助かります。",
            "concise": "締切を2日延長いただけますでしょうか。",
            "highly_professional": "誠に恐縮ですが、締切につき2日間のご猶予を賜れますと幸甚です。",
        },
        "meta": {"intent": "request_extension", "ambiguity": "", "confidence": 0.9, "warnings": []},
        "safety_flags": {"ambiguous_input": False, "missing_context": False, "potentially_risky": False},
    }
    with patch("app.main.generate_polish_result", return_value=mocked_response):
        res = client.post(
            "/api/v1/polish",
            json={
                "language": "ja",
                "original_message": "締切を2日延ばしたいです",
                "recipient_type": "professor",
                "tone": "formal",
                "purpose": "request_extension",
            },
        )
    assert res.status_code == 200
    body = res.json()
    assert body["rewritten_message"]
    assert set(body["quick_variants"].keys()) == {
        "formal",
        "friendly",
        "concise",
        "highly_professional",
    }
