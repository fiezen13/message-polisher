# Message Polisher

Tool nhỏ để **chỉnh tin nhắn công việc sang tiếng Nhật** theo ngữ cảnh bạn chọn (ai nhận, tone, mục đích, mức chi tiết). Bạn có thể gõ **tiếng Việt** ở đầu vào, kết quả mặc định là **tiếng Nhật**.

Mục tiêu: hỗ trợ message kiểu email/chat nội bộ (giáo viên, recruiter, quản lý, khách hàng) thay vì “paraphrase chung chung”.

## Bạn sẽ nhận được gì

Khi gọi API (hoặc dùng UI), response thường gồm:

- Một bản chính: `rewritten_message`
- Bốn biến thể nhanh: `quick_variants` (formal / friendly / concise / highly_professional)
- Một chút metadata: `meta` và `safety_flags` (cảnh báo mức độ mơ hồ, thiếu context, v.v.)

Lưu ý: chất lượng phụ thuộc model/provider và cách bạn chọn `tone/purpose/detail_level`. Nếu output vẫn “dịch cứng”, thử tăng `detail_level` hoặc đổi `tone/purpose` cho sát tình huống hơn.

## Cách dùng nhanh (không cần đọc phần API)

### 1) Cài dependency

Yêu cầu: Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### 2) Cấu hình API key (Groq)

Ứng dụng cần biến môi trường `GROQ_API_KEY`.

Cách phổ biến: tạo file `.env` ở thư mục gốc repo (file này đang được ignore, đừng commit):

```bash
GROQ_API_KEY=...
```

### 3) Chạy giao diện (Streamlit)

```bash
streamlit run scripts/web_ui.py
```

Trong form:

- `Source language`: thường chọn `vi` nếu bạn gõ tiếng Việt
- `Recipient / Tone / Purpose`: chọn cho đúng tình huống
- `Detail level`:
  - `concise`: câu ngắn, ưu tiên xin phép/đi thẳng ý
  - `balanced`: mặc định, cân bằng
  - `detailed`: cho phép giải thích rõ hơn nếu cần

Nếu bạn vừa cập nhật code mà UI báo lỗi kiểu `unexpected keyword argument ...`, dừng hẳn Streamlit (Ctrl+C) rồi chạy lại để reload module.

## Dành cho developer (tích hợp / tự host)

### Chạy API local

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Health: `GET /health`
- Swagger: `/docs`

### Endpoint chính

`POST /api/v1/polish`

Ví dụ payload:

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

`language` hiện đang cố định là `ja` (output). `source_language` cho biết ngôn ngữ đầu vào.

### CLI (pipeline cũ, đơn giản)

```bash
python scripts/message_cli.py
```

CLI này đi theo `style_mode` kiểu `neutral_business / formal_keigo / casual_polite`, không phản ánh đầy đủ UI/API mới.

## Kiểm thử

```bash
pytest
```

## Script eval trong repo (đọc kỹ trước khi tin số liệu)

`scripts/evaluate.py` + `eval/eval_cases.json` hiện đánh giá theo `generate_polished_message` (legacy). Nó **chưa khớp hoàn toàn** contract `/api/v1/polish`, nên phù hợp smoke test nhanh hơn là benchmark sản phẩm.

## Trạng thái dự án (thẳng thắn)

Phù hợp demo/MVP nội bộ: có UI, có API, có test cơ bản.

Chưa gọi là production-ready nếu bạn public deploy: chưa có auth, rate limit, logging/observability đầy đủ, packaging/deploy chuẩn (Docker/CI) trong repo.

## License

Chưa đặt. Thêm `LICENSE` nếu bạn open-source.
