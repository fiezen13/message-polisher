# Message Polisher

Ứng dụng chỉnh tin nhắn sang tiếng Nhật theo ngữ cảnh (người nhận, tone, mục đích, mức chi tiết). Hỗ trợ đầu vào `vi` / `ja` / `en`, output hiện cố định `ja`.

## Yêu cầu

- Python 3.10+
- Biến môi trường `GROQ_API_KEY`

## Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Kích hoạt venv trên Windows:

```text
.venv\Scripts\activate
```

Tạo `.env` ở thư mục gốc repo (đã ignore, không commit):

```bash
GROQ_API_KEY=...
```

## Chạy UI (Streamlit)

```bash
streamlit run scripts/web_ui.py
```

Form tương ứng các field: `source_language`, `recipient_type`, `tone`, `purpose`, `detail_level`.

Nếu đổi code Python mà Streamlit báo lỗi kiểu `unexpected keyword argument ...`, dừng tiến trình (Ctrl+C) rồi chạy lại.

## Chạy API (FastAPI)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- `GET /health`
- Swagger: `/docs`
- Endpoint: `POST /api/v1/polish`

Ví dụ body:

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

`language` chỉ nhận `ja`. `detail_level` mặc định `balanced` nếu không gửi.

## Response

- `rewritten_message`
- `quick_variants`: `formal`, `friendly`, `concise`, `highly_professional`
- `meta`, `safety_flags`

## CLI (legacy)

```bash
python scripts/message_cli.py
```

Pipeline theo `style_mode` (`neutral_business`, `formal_keigo`, `casual_polite`), không tương đương hoàn toàn UI/API mới.

## Test

```bash
pytest
```

## Eval (legacy)

```bash
python scripts/evaluate.py
```

Script này gắn với `generate_polished_message` và `eval/eval_cases.json`, không đồng bộ hoàn toàn với `/api/v1/polish`.

## Trạng thái

Phù hợp chạy local / demo. Chưa bao gồm các phần production đầy đủ (auth, rate limit, observability, CI/CD, container).

## License

Chưa có. Thêm `LICENSE` nếu công khai mã nguồn.
