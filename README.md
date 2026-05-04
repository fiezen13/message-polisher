# Message Polisher

Ứng dụng hỗ trợ viết lại tin nhắn công việc theo **ngữ cảnh** (recipient / tone / purpose), ưu tiên **tiếng Nhật**, có thể nhận input **tiếng Việt** và trả output **tiếng Nhật**.

## Tính năng hiện tại

- **Polish theo ngữ cảnh**: `recipient_type`, `tone`, `purpose`, `detail_level`.
- **Đa ngôn ngữ nguồn**: `source_language` (`vi`, `ja`, `en`) với output `language` hiện cố định `ja`.
- **Kết quả có cấu trúc**:
  - `rewritten_message`
  - `quick_variants` (`formal`, `friendly`, `concise`, `highly_professional`)
  - `meta`, `safety_flags`
- **API**: FastAPI (`POST /api/v1/polish`, `GET /health`).
- **Web UI**: Streamlit (`scripts/web_ui.py`) để test nhanh.
- **CLI cũ** (rewrite đơn giản theo `style_mode`): `scripts/message_cli.py`.
- **Tests**: `pytest`.

## Kiến trúc (tóm tắt)

- `app/main.py`: FastAPI app + endpoint.
- `app/api/schemas.py`: Pydantic request/response.
- `app/services/ai_service.py`: orchestration (intent -> rewrite -> variants).
- `app/services/context_resolver.py`: resolve guidance theo recipient/tone/purpose/detail.
- `app/core/config.py`: policy text + prompt templates.

## Yêu cầu môi trường

- Python 3.10+ (repo hiện đang test trên 3.10).
- Groq API key: `GROQ_API_KEY`.

## Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Tạo file `.env` ở **thư mục gốc repo** (khuyến nghị) hoặc đặt biến môi trường trực tiếp:

```bash
export GROQ_API_KEY="your_key_here"
```

Lưu ý: không commit file chứa secret. Repo đã ignore `.env` (xem `.gitignore`).

## Chạy API (FastAPI)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Health: `GET http://127.0.0.1:8000/health`
- Docs: `http://127.0.0.1:8000/docs`

### Ví dụ request `POST /api/v1/polish`

```json
{
  "language": "ja",
  "source_language": "vi",
  "original_message": "Em muốn xin lùi deadline thêm 2 ngày vì bận học nhiều môn trên trường",
  "recipient_type": "professor",
  "tone": "apologetic",
  "purpose": "request_extension",
  "detail_level": "detailed"
}
```

## Chạy Web UI (Streamlit)

```bash
streamlit run scripts/web_ui.py
```

Nếu bạn vừa sửa signature Python (ví dụ thêm field mới) mà UI báo lỗi kiểu `unexpected keyword argument`, hãy **dừng hẳn** Streamlit rồi chạy lại để reload module.

## Chạy tests

```bash
pytest
```

## Eval script (legacy)

`scripts/evaluate.py` hiện đánh giá theo pipeline cũ `generate_polished_message` + `eval/eval_cases.json`. Nó **chưa** reflect đầy đủ contract mới (`/api/v1/polish`). Dùng để smoke test nhanh, không nên coi là benchmark chính thức cho product mới cho đến khi được nâng cấp.

## Mức độ “hoàn thiện” (thực tế)

Hiện tại phù hợp mục tiêu **MVP nội bộ / demo có giá trị**:

- Đã có product loop cơ bản: UI/API -> model -> variants -> meta.
- Đã có tests tự động cho API + resolver + một phần pipeline.

Chưa đủ mức production-ready nếu bạn muốn public deploy:

- chưa có auth/rate limit/cost control,
- chưa có observability chuẩn (structured logging, tracing),
- eval/benchmark cho contract mới chưa đồng bộ,
- chưa có packaging/deploy (Docker/CI) trong repo.

## License

Chưa khai báo. Thêm file license nếu bạn open-source.
